"""
Collision model generation logic.
"""
import bpy  # type: ignore
import bmesh  # type: ignore


def get_skinned_meshes(armature) -> list:
    """
    Get all meshes that are skinned to an armature.
    
    Args:
        armature: The armature object
    
    Returns:
        list: List of mesh objects controlled by the armature
    """
    controlled_meshes = []
    
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            for mod in obj.modifiers:
                if mod.type == 'ARMATURE' and mod.object == armature:
                    controlled_meshes.append(obj)
                    break
    
    return controlled_meshes


def get_vertices_by_highest_weight(obj) -> dict:
    """
    Get all vertices grouped by their highest-weighted vertex group.
    
    Args:
        obj: The mesh object
    
    Returns:
        dict: Dictionary mapping vertex group names to lists of world-space coordinates
    """
    mesh_data = obj.data
    vertex_groups = obj.vertex_groups
    vgroups = {}
    
    index_to_name = {vg.index: vg.name for vg in vertex_groups}
    
    for vg in vertex_groups:
        vgroups[vg.name] = []
    
    for v in mesh_data.vertices:
        if not v.groups:
            continue
        
        highest_influence = max(v.groups, key=lambda g: g.weight)
        group_name = index_to_name[highest_influence.group]
        world_co = obj.matrix_world @ v.co.copy()
        vgroups[group_name].append(world_co)
    
    return vgroups


def generate_collision_bounds(vertex_groups_dict: dict, obj) -> dict:
    """
    Generate bounding box corners for each vertex group.
    
    Args:
        vertex_groups_dict: Dictionary from get_vertices_by_highest_weight
        obj: The mesh object
    
    Returns:
        dict: Dictionary mapping vertex group names to corner positions
    """
    collision_bounds = {}
    
    for vgroup_name, data in vertex_groups_dict.items():
        if not data:
            continue
        
        x_coords = []
        y_coords = []
        z_coords = []
        
        for v in data:
            world_co = obj.matrix_world @ v
            x_coords.append(world_co.x)
            y_coords.append(world_co.y)
            z_coords.append(world_co.z)
        
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        min_z, max_z = min(z_coords), max(z_coords)
        
        corners = {
            "0_bottom_back_right": (max_x, min_y, min_z),
            "1_bottom_front_right": (max_x, max_y, min_z),
            "2_bottom_front_left": (min_x, max_y, min_z),
            "3_bottom_back_left": (min_x, min_y, min_z),
            "4_top_back_right": (max_x, min_y, max_z),
            "5_top_front_right": (max_x, max_y, max_z),
            "6_top_front_left": (min_x, max_y, max_z),
            "7_top_back_left": (min_x, min_y, max_z),
        }
        
        collision_bounds[vgroup_name] = corners
    
    return collision_bounds


def create_collision_boxes(
    collision_bounds: dict,
    collection_name: str = "collisions",
    wireframe: bool = False,
    prefix: str = "CollisionCube"
) -> list:
    """
    Create collision box meshes from bounding box data.
    
    Args:
        collision_bounds: Dictionary from generate_collision_bounds
        collection_name: Name of the collection to place boxes in
        wireframe: Whether to display as wireframe
        prefix: Prefix for collision object names
    
    Returns:
        list: List of created objects
    """
    # Get or create collection
    collisions_col = bpy.data.collections.get(collection_name)
    if collisions_col is None:
        collisions_col = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(collisions_col)
    
    created_objs = []
    
    for vgroup_name, corners in collision_bounds.items():
        verts_coords = [
            corners["0_bottom_back_right"],
            corners["1_bottom_front_right"],
            corners["2_bottom_front_left"],
            corners["3_bottom_back_left"],
            corners["4_top_back_right"],
            corners["5_top_front_right"],
            corners["6_top_front_left"],
            corners["7_top_back_left"],
        ]
        
        face_indices = [
            (0, 1, 2, 3),
            (4, 5, 6, 7),
            (0, 4, 5, 1),
            (1, 5, 6, 2),
            (2, 6, 7, 3),
            (3, 7, 4, 0)
        ]
        
        mesh = bpy.data.meshes.new(f"collision_cube_{vgroup_name}")
        bm = bmesh.new()
        bm_verts = [bm.verts.new(co) for co in verts_coords]
        bm.verts.ensure_lookup_table()
        
        for fi in face_indices:
            face = bm.faces.new([bm_verts[i] for i in fi])
            face.smooth = True
        
        bm.to_mesh(mesh)
        bm.free()
        
        obj = bpy.data.objects.new(f"{prefix}_{vgroup_name}", mesh)
        collisions_col.objects.link(obj)
        
        if wireframe:
            obj.display_type = 'WIRE'
            try:
                obj.color = (0.0, 1.0, 0.0, 0.25)
            except Exception:
                pass
        
        created_objs.append(obj)
    
    return created_objs


def parent_collision_to_bones(armature_obj, prefix: str = "CollisionCube_") -> None:
    """
    Parent collision cubes to their corresponding bones.
    
    Args:
        armature_obj: The armature object
        prefix: Prefix used for collision cube names
    """
    if armature_obj.type != 'ARMATURE':
        print(f"{armature_obj.name} is not an armature object.")
        return
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    for obj in bpy.data.objects:
        if not obj.name.startswith(prefix):
            continue
        
        bone_name = obj.name[len(prefix):]
        
        if bone_name not in armature_obj.data.bones:
            print(f"Bone '{bone_name}' not found for object '{obj.name}'")
            continue
        
        obj.parent = armature_obj
        obj.parent_type = 'BONE'
        obj.parent_bone = bone_name
        obj.matrix_parent_inverse = armature_obj.matrix_world.inverted()
        
        print(f"Parented '{obj.name}' → bone '{bone_name}'")
    
    print("Parenting complete.")


def create_collisions_for_armatures(armature_list: list) -> None:
    """
    Create collision boxes for all meshes skinned to the given armatures.
    
    Args:
        armature_list: List of armature objects
    """
    for armature in armature_list:
        skinned_meshes = get_skinned_meshes(armature)
        
        for mesh in skinned_meshes:
            highest_groups = get_vertices_by_highest_weight(mesh)
            collision_bounds = generate_collision_bounds(highest_groups, mesh)
            create_collision_boxes(collision_bounds)
            parent_collision_to_bones(armature)
