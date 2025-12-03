import bpy, bmesh # type: ignore
from mathutils import Vector # type: ignore
from . import von_deltaanimtrick
from . import von_common

#-------------------------------------------------------------------------------------------------------------------------------------------------
# Delta Anim Trick
#-------------------------------------------------

def has_properties():
    print("-----------------------Running Has_Properties -----------------------")
    hasProportions = bpy.data.objects.get("proportions")
    hasMaleRef = bpy.data.objects.get("reference_female")
    hasFemaleRef = bpy.data.objects.get("reference_male")

    if hasProportions:
        for col in hasProportions.users_collection:
            col.objects.unlink(hasProportions)
        bpy.data.objects.remove(hasProportions)
        von_common.importitemfromdict("proportions", "Collection 2", von_common.deltaanimtrick_armaturefilelocations())
        hasProportions = True
    else:
        von_common.importitemfromdict("proportions", "Collection 2", von_common.deltaanimtrick_armaturefilelocations())
        hasProportions = True
    if not hasFemaleRef:
        von_common.importitemfromdict("reference_female", "Collection 3", von_common.deltaanimtrick_armaturefilelocations())
        hasFemaleRef = True
    else:
        hasFemaleRef = True
    if not hasMaleRef:
        von_common.importitemfromdict("reference_male", "Collection 3", von_common.deltaanimtrick_armaturefilelocations())
        hasMaleRef = True
    else:
        hasMaleRef = True

    print(hasProportions, hasMaleRef, hasFemaleRef)
    bpy.data.objects.get("proportions").select_set(False)
    return hasProportions, hasMaleRef, hasFemaleRef

def is_valve_biped(armature, context):
    print("----------------------- Running Is_Valve_Biped -----------------------")
    scene = context.scene
    toolBox = scene.toolBox

    itteration:float = 0
    simmilarityThreshold:float = 0

    armatureBones = armature.data.bones
    simmilarityThreshold = toolBox.float_deltaAnim_simmilarityThreshold

    for bone in armatureBones:
        if bone.name in von_common.deltaanimtrick_valvebipeds_1():
            if "_end" in bone.name:
                pass
            else:
                itteration += 1.0
    
    matchingPercentage = itteration / float(len(armatureBones))
    matchingPercentage = matchingPercentage * 100

    if matchingPercentage >= simmilarityThreshold:
        return True
    else:
        return False
            
class Vonpanel_DeltaAnimTrick_ImportRequiredProperties(bpy.types.Operator):
    bl_idname = "von.deltaanimtrick_importrequiredproperties"
    bl_label = "Import Required Armatures"
    def execute(self,context):
        print("-----------------------Running Import Required Properties -----------------------")
        hasProportions, hasMaleRef, hasFemaleRef = has_properties()
        try:
            print(f"hasProportions = {hasProportions} ||| hasMaleRef = {hasMaleRef} ||| hasFemaleRef = {hasFemaleRef}")
        except:
            return{'CANCELLED'}
        return{'FINISHED'}

class VonPanel_DeltaAnimTrick_PartOne(bpy.types.Operator):
    bl_idname = "von.deltaanimtrick_partone"
    bl_label = "Delta Anim Trick (One)"
    def execute(self, context):
        print("-----------------------Running Delta Anim Trick 1 -----------------------")
        #Import reference armatures
        hasProportions: bool = False
        hasMaleRef: bool = False
        hasFemaleRef: bool = False

        hasProportions, hasMaleRef, hasFemaleRef = has_properties()

        if hasProportions and hasMaleRef and hasFemaleRef:
            #Get selected armatures
            obj = [obj for obj in bpy.data.objects if obj.type == "ARMATURE"]
            #Run once on each valid armature
            for armature in obj:
                von_deltaanimtrick.delta_anim_trick_one(armature)
            return{"FINISHED"}
        return{'CANCELLED'}

class VonPanel_DeltaAnimTrick_PartTwo(bpy.types.Operator):
    bl_idname = "von.deltaanimtrick_parttwo"
    bl_label = "Delta Anim Trick (Two)"
    def execute(self, context):
        print("-----------------------Running Delta Anim Trick 2 -----------------------")
        #Import reference armatures
        hasProportions: bool = False
        hasMaleRef: bool = False
        hasFemaleRef: bool = False
        hasProportions, hasMaleRef, hasFemaleRef = has_properties()

        if hasProportions and hasMaleRef and hasFemaleRef:
            #Get selected armatures
            obj = [obj for obj in bpy.data.objects if obj.type == "ARMATURE"]
            #Run once on each valid armature
            for armature in obj:
                von_deltaanimtrick.delta_anim_trick_two(armature.name)
            return{"FINISHED"}
        return{'CANCELLED'}

class VonPanel_DeltaAnimTrick_Full(bpy.types.Operator):
    bl_idname = "von.deltaanimtrick_full"
    bl_label = "Delta Anim Trick (Full)"
        

    def execute(self, context):
        print("-----------------------Running Delta Anim Trick FULL -----------------------")
        scene = context.scene
        toolBox = scene.toolBox

        failures:list = []
        hasvalvepiedarmature:bool = True

        obj = [obj for obj in bpy.context.selected_objects if obj.type == "ARMATURE"]
        firstobj = obj[0]
        if not obj:
            self.report({'ERROR'}, f"No Armature Detected")
            return{'CANCELLED'}

        for armature in obj:
            if is_valve_biped(armature, context):
                pass
            else:
                hasvalvepiedarmature = False
                failures.append(armature)
        if hasvalvepiedarmature == False:
            for failure in failures:
                self.report({'ERROR'}, f"{failure.name} has failed to meet the current simmilarity threshold of {toolBox.float_deltaAnim_simmilarityThreshold} | Please either lower threshold or ensure the armature uses valve biped armature on core deformation bones.")
            return{'CANCELLED'}
        
        firstobj.select_set(True)

        

        print("Checkpoint 1")
        #Import reference armatures
        hasProportions: bool = False
        hasMaleRef: bool = False
        hasFemaleRef: bool = False
        hasProportions, hasMaleRef, hasFemaleRef = has_properties()
        von_common.reselect_all(obj, obj[0])

        if hasProportions and hasMaleRef and hasFemaleRef:
            for armatureDataBlock in obj:
                print(armatureDataBlock)
                bpy.context.view_layer.objects.active = obj[0]

                print("Checkpoint 2")
                bpy.ops.object.mode_set(mode='EDIT')
                editbones = armatureDataBlock.data.edit_bones
                bpy.ops.object.mode_set(mode='POSE')

                armatureobject = bpy.data.objects[armatureDataBlock.name]
                posebones = armatureobject.pose.bones

                von_deltaanimtrick.delta_anim_trick_one(armatureDataBlock)



                #NEEDS TO ONLY AFFECT PROPORTIONS BONES
                proportionsArmature = bpy.data.objects["proportions"]
                bpy.context.view_layer.objects.active = proportionsArmature
                bpy.ops.object.mode_set(mode='EDIT')
                proportionsEditBones = proportionsArmature.data.edit_bones
                for bone in proportionsEditBones:
                    if bone.name == "ValveBiped.Bip01_L_Toe0" or bone.name == "ValveBiped.Bip01_L_Toe0":
                        von_deltaanimtrick.toevertical(bone)
            
                
                

                bpy.context.view_layer.objects.active = proportionsArmature
                bpy.ops.object.mode_set(mode='POSE')
                proportionsPoseBones = proportionsArmature.pose.bones
                bpy.ops.pose.armature_apply(selected=False)
                for bone in proportionsPoseBones:
                    von_deltaanimtrick.clearposeboneconstraints(bone, proportionsArmature)
                
                von_deltaanimtrick.delta_anim_trick_two(armature.name)
            bpy.context.view_layer.objects.active = proportionsArmature
            bpy.ops.object.mode_set(mode='OBJECT')
            self.report({'INFO'}, "Delta Anim Trick Successful | Test in HLMV and use advanced process if unsucessful")
            return{"FINISHED"}
        return{'CANCELLED'}

#-------------------------------------------------------------------------------------------------------------------------------------------------
# QC Generator Script
#-------------------------------------------------

for section in sections:
    sectionCommand = f"${section}"
    


#"PROP": {
        #    "flags": ["$staticprop"],
        #    "sections": ["modelname", "cdmaterials", "bodygroup", "sequence", "collisionmodel"]
def get_skinned_meshes(armature):
    controlled_meshes = []
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            for mod in obj.modifiers:
                if mod.type == 'ARMATURE' and mod.object == armature:
                    controlled_meshes.append(obj)
                    break
    return controlled_meshes

def getallvertices_highest_vertexgroups_and_vert_location(ob):
    me = ob.data
    vertexgroups = ob.vertex_groups
    vgroups:dict = {}
    index_to_name = {vg.index: vg.name for vg in vertexgroups}   
    for vg in vertexgroups:
        vgroups[vg.name] = []
    for v in me.vertices:
        if not v.groups:
            continue
        highestInfluence = max(v.groups, key=lambda g: g.weight)
        group_name = index_to_name[highestInfluence.group]
        world_co = ob.matrix_world @ v.co.copy()
        vgroups[group_name].append(world_co)
    for key, data in vgroups.items():
        print(key)
        for vector in data:
            print(vector)
    return vgroups



def generate_collission_model_data(dictHighestVertexGroupPerVert:dict, obj):
    dict_collission_bounds:dict = {}
    for vGroup, data in dictHighestVertexGroupPerVert.items():
        if not data:
            continue
        xCords = []
        yCords = []
        zCords = []
        for v in data:
            world_co = obj.matrix_world @ v
            xCords.append(world_co.x)
            yCords.append(world_co.y)
            zCords.append(world_co.z)

        minX, maxX = min(xCords), max(xCords)
        minY, maxY = min(yCords), max(yCords)
        minZ, maxZ = min(zCords), max(zCords)
        
        corners = {
            "0_bottom_back_right"  : (maxX, minY, minZ),
            "1_bottom_front_right" : (maxX, maxY, minZ),
            "2_bottom_front_left"  : (minX, maxY, minZ),
            "3_bottom_back_left"   : (minX, minY, minZ),
            "4_top_back_right"     : (maxX, minY, maxZ),
            "5_top_front_right"    : (maxX, maxY, maxZ),
            "6_top_front_left"     : (minX, maxY, maxZ),
            "7_top_back_left"      : (minX, minY, maxZ),
        }

        dict_collission_bounds[vGroup] = corners
    return dict_collission_bounds

def create_collision_boxes_correct(dict_collision_bounds:dict, collection_name:str="collisions", wireframe:bool=False, prefix:str = "CollisionCube"):
    for vGroup, corners in dict_collision_bounds.items():
        print(vGroup)
        for vertexpos, vector in corners.items():
            print(vertexpos)
            print(vector)


    collisions_col = bpy.data.collections.get(collection_name)
    if collisions_col is None:
        collisions_col = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(collisions_col)

    created_objs = []

    for vGroup, corners in dict_collision_bounds.items():
        verts_coords = [
            corners["0_bottom_back_right"],  # 0
            corners["1_bottom_front_right"],  # 1
            corners["2_bottom_front_left"],  # 2
            corners["3_bottom_back_left"],  # 3
            corners["4_top_back_right"],  # 4
            corners["5_top_front_right"],  # 5
            corners["6_top_front_left"],  # 6
            corners["7_top_back_left"],  # 7
        ]

        # Faces with "correct" loop ordering
        face_indices = [
            (0, 1, 2, 3),
            (4, 5, 6, 7),
            (0, 4, 5, 1),
            (1, 5, 6, 2),
            (2, 6, 7, 3),
            (3, 7, 4, 0)
        ]

        # Create mesh and BMesh
        mesh = bpy.data.meshes.new(f"collision_cube_{vGroup}")
        bm = bmesh.new()
        bm_verts = [bm.verts.new(co) for co in verts_coords]
        bm.verts.ensure_lookup_table()

        # Create faces and set smooth shading
        for fi in face_indices:
            face = bm.faces.new([bm_verts[i] for i in fi])
            face.smooth = True
        # Write BMesh to mesh
        bm.to_mesh(mesh)
        bm.free()

        # Create object
        obj = bpy.data.objects.new(f"{prefix}_{vGroup}", mesh)
        collisions_col.objects.link(obj)

        # Optional wireframe display
        if wireframe:
            obj.display_type = 'WIRE'
            try:
                obj.color = (0.0, 1.0, 0.0, 0.25)
            except Exception:
                pass

        created_objs.append(obj)

    return created_objs


def parent_collision_cubes_to_bones(armature_obj, prefix="CollisionCube_"):
    # Make sure this is an armature
    if armature_obj.type != 'ARMATURE':
        print(f"{armature_obj.name} is not an armature object.")
        return

    # Put the armature in object mode to avoid parenting issues
    bpy.ops.object.mode_set(mode='OBJECT')

    # Iterate through all objects in the scene
    for obj in bpy.data.objects:
        if not obj.name.startswith(prefix):
            continue

        # Extract the bone name after the prefix
        bone_name = obj.name[len(prefix):]

        # Check if the bone exists
        if bone_name not in armature_obj.data.bones:
            print(f"Bone '{bone_name}' not found for object '{obj.name}'")
            continue

        # Parent the cube to the armature (bone parent type)
        obj.parent = armature_obj
        obj.parent_type = 'BONE'
        obj.parent_bone = bone_name

        # Reset local transforms so the cube stays in place
        obj.matrix_parent_inverse = armature_obj.matrix_world.inverted()

        print(f"Parented '{obj.name}' → bone '{bone_name}'")

    print("Parenting complete.")



class Vonpanel_qcgenerator_prop(bpy.types.Operator):
    bl_idname = "von.qcgenerator_prop"
    bl_label = "Generate QC File"
    def execute(self,context):
        scene = context.scene
        toolBox = scene.toolBox
        modelname = toolBox.string_qcGen_mdlModelName
        qc_output = toolBox.string_qcGen_outputPath
        shouldGenCollis = toolBox.bool_qcGen_generateCollission
        selected_armatures = [obj for obj in context.selected_objects if obj.type == 'ARMATURE']

        #Generate Collissions
        if shouldGenCollis:
            for armature in selected_armatures:
                for mesh in get_skinned_meshes(armature):
                    vertDict = getallvertices_highest_vertexgroups_and_vert_location(mesh)
                    collisData = generate_collission_model_data(vertDict, mesh)
                    create_collision_boxes_correct(collisData)
        if not shouldGenCollis:
            collisCollection = toolBox.string_qcGen_existingCollissionCollection
        
        #Get QC_Type
        qcType = toolBox.enum_qcGen_modelType
        qcFlags = von_common.qc_file_types()
        qcFlags = qcFlags[qcType]


        #"PROP": {
        #    "flags": ["$staticprop"],
        #    "sections": ["$modelname", "$cdmaterials", "$bodygroup", "$sequence", "$collisionmodel"]

        for flag, section in qcFlags:
            populate_qc_dict_from_sections()


        return{'FINISHED'}

class Vonpanel_qcgenerator_player(bpy.types.Operator):
    bl_idname = "von.qcgenerator_player"
    bl_label = "Generate QC File"
    def execute(self,context):
        scene = context.scene
        toolBox = scene.toolBox
        modelname = toolBox.string_qcGen_mdlModelName
        qc_output = toolBox.string_qcGen_outputPath
        shouldGenCollis = toolBox.bool_qcGen_generateCollission
        return{'FINISHED'}

class Vonpanel_qcgenerator_npc(bpy.types.Operator):
    bl_idname = "von.qcgenerator_npc"
    bl_label = "Generate QC File"
    def execute(self,context):
        scene = context.scene
        toolBox = scene.toolBox
        modelname = toolBox.string_qcGen_mdlModelName
        qc_output = toolBox.string_qcGen_outputPath
        shouldGenCollis = toolBox.bool_qcGen_generateCollission
        return{'FINISHED'}
class Vonpanel_RefreshCollections(bpy.types.Operator):
    bl_idname = "von.qcgenerator_refresh_collections"
    bl_label = "Refresh Collection List"

    def execute(self, context):
        scene = context.scene
        von_common.sync_bodygroup_boxes(scene)
        self.report({'INFO'}, "Collections synced with scene.")
        return {'FINISHED'}
        


# ----------------------------------------------------------------------------------------------------------------------------------------------------
# Register Fnction
# ----------------------------


classes = (
    #Delta Anim
    Vonpanel_DeltaAnimTrick_ImportRequiredProperties,
    VonPanel_DeltaAnimTrick_PartOne,
    VonPanel_DeltaAnimTrick_PartTwo,
    VonPanel_DeltaAnimTrick_Full,
    #QC Gen
    Vonpanel_qcgenerator_prop,
    Vonpanel_qcgenerator_player,
    Vonpanel_qcgenerator_npc,
    Vonpanel_RefreshCollections
)


def von_operator_register():
    for cls in classes:
        bpy.utils.register_class(cls)    


def von_operator_unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)