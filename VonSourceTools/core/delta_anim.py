"""
Delta Animation Trick core logic.

Credit: Original proportion trick script from https://github.com/sksh70/proportion_trick_script
This implementation is modified from Blender 2.9 with additional automation.
"""
import bpy  # type: ignore
from collections import OrderedDict

from ..data.valvebiped_bones import VALVEBIPED_BONES, VALVEBIPED_CONSTRAINT_PAIRS
from ..data.paths import get_armature_file_locations
from ..utils.blender_utils import move_to_collection, object_exists, select_objects


def import_reference_armatures() -> tuple:
    """
    Import the required reference armatures for the delta animation trick.
    
    Returns:
        tuple: (has_proportions, has_male_ref, has_female_ref)
    """
    armature_locations = get_armature_file_locations()
    
    # Handle proportions armature
    proportions = bpy.data.objects.get("proportions")
    if proportions:
        for col in proportions.users_collection:
            col.objects.unlink(proportions)
        bpy.data.objects.remove(proportions)
    
    _import_fbx_armature("proportions", "Collection 2", armature_locations)
    has_proportions = True
    
    # Handle reference_female armature
    if not bpy.data.objects.get("reference_female"):
        _import_fbx_armature("reference_female", "Collection 3", armature_locations)
    has_female_ref = True
    
    # Handle reference_male armature
    if not bpy.data.objects.get("reference_male"):
        _import_fbx_armature("reference_male", "Collection 3", armature_locations)
    has_male_ref = True
    
    # Deselect proportions
    proportions_obj = bpy.data.objects.get("proportions")
    if proportions_obj:
        proportions_obj.select_set(False)
    
    return has_proportions, has_male_ref, has_female_ref


def _import_fbx_armature(name: str, collection: str, armature_dict: dict) -> None:
    """
    Import an FBX armature and move it to a collection.
    
    Args:
        name: Name of the armature to import
        collection: Target collection name
        armature_dict: Dictionary mapping names to file paths
    """
    filepath = armature_dict.get(name)
    if not filepath:
        raise ImportError(f"Armature '{name}' not found in dictionary")
    
    try:
        bpy.ops.import_scene.fbx(filepath=str(filepath))
    except Exception as e:
        raise ImportError(f"Failed to import '{name}': {e}")
    
    move_to_collection(name, collection)


def validate_valvebiped_similarity(armature, threshold: float = 90.0) -> bool:
    """
    Check if an armature matches the ValveBiped skeleton structure.
    
    Args:
        armature: The armature object to check
        threshold: Minimum percentage of bones that must match (0-100)
    
    Returns:
        bool: True if armature meets threshold, False otherwise
    """
    if armature.type != 'ARMATURE':
        return False
    
    armature_bones = armature.data.bones
    matching_count = 0
    
    for bone in armature_bones:
        if bone.name in VALVEBIPED_BONES and "_end" not in bone.name:
            matching_count += 1
    
    matching_percentage = (matching_count / len(armature_bones)) * 100
    return matching_percentage >= threshold


def delta_anim_part_one(source_armature: bpy.types.Object) -> None:
    """
    Execute the first part of the delta animation trick.
    Sets up constraints on the proportions armature to match the source.
    
    Args:
        source_armature: The source armature object
    """
    if 'proportions' not in bpy.data.objects:
        raise Exception("No armature named 'proportions' found in the scene.")
    
    target_armature = bpy.data.objects['proportions']
    
    if isinstance(source_armature, str):
        source_armature = bpy.data.objects[source_armature]
    
    if target_armature.type != 'ARMATURE':
        raise TypeError(f"Target armature 'proportions' must be an ARMATURE, not {target_armature.type}")
    if source_armature.type != 'ARMATURE':
        raise TypeError(f"Source armature must be an ARMATURE, not {source_armature.type}")
    
    # Build bone mapping for locked track constraints
    target_bones = VALVEBIPED_CONSTRAINT_PAIRS[::2]
    sub_bones = VALVEBIPED_CONSTRAINT_PAIRS[1::2]
    bone_mapping = OrderedDict()
    for idx, value in enumerate(sub_bones):
        bone_mapping[f'var{idx}'] = value
    
    # Add Copy Location constraints
    for bone_name in VALVEBIPED_BONES:
        if bone_name not in target_armature.pose.bones:
            continue
        
        target_bone = target_armature.pose.bones[bone_name].constraints
        
        if 'Copy Location' not in target_bone:
            c = target_bone.new('COPY_LOCATION')
            c.name = 'Copy Location'
            c.target = source_armature
            c.subtarget = bone_name
    
    # Add Locked Track constraints
    for idx, bone_name in enumerate(target_bones):
        if bone_name not in target_armature.pose.bones:
            continue
        
        target_bone = target_armature.pose.bones[bone_name].constraints
        
        c1 = target_bone.new('LOCKED_TRACK')
        c1.name = 'Locked Track_XZ'
        c1.target = source_armature
        c1.subtarget = bone_mapping[f'var{idx}']
        c1.track_axis = 'TRACK_X'
        c1.lock_axis = 'LOCK_Z'
        
        c2 = target_bone.new('LOCKED_TRACK')
        c2.name = 'Locked Track_XY'
        c2.target = source_armature
        c2.subtarget = bone_mapping[f'var{idx}']
        c2.track_axis = 'TRACK_X'
        c2.lock_axis = 'LOCK_Y'
    
    # Clean up constraints on childless bones
    for bone_name in VALVEBIPED_BONES:
        if bone_name not in target_armature.pose.bones:
            continue
        
        parent_bone = target_armature.pose.bones[bone_name]
        
        for child in parent_bone.children:
            child_constraints = target_armature.pose.bones[child.name].constraints
            if not child_constraints.keys():
                for constraint in parent_bone.constraints:
                    if constraint.type != 'COPY_LOCATION':
                        parent_bone.constraints.remove(constraint)
    
    # Set visibility and selection
    target_armature.hide_set(False)
    source_armature.hide_set(True)
    bpy.context.view_layer.objects.active = target_armature
    target_armature.select_set(True)
    bpy.ops.object.mode_set(mode='POSE')
    
    print(f"'proportions' aligned to {source_armature.name} successfully!")


def delta_anim_part_two(imported_name: str = "gg", proportions_name: str = "proportions") -> None:
    """
    Execute the second part of the delta animation trick.
    Merges non-ValveBiped bones and updates armature modifiers.
    
    Args:
        imported_name: Name of the imported skeleton
        proportions_name: Name of the proportions armature
    """
    objects = bpy.data.objects
    
    if imported_name not in objects:
        raise Exception(f"{imported_name} skeleton not found. Rename imported skeleton to '{imported_name}'.")
    if proportions_name not in objects:
        raise Exception(f"{proportions_name} object not found in scene.")
    
    arm = objects[imported_name]
    arm2 = objects[proportions_name]
    
    if arm.type != 'ARMATURE':
        raise Exception(f"{imported_name} must be an ARMATURE, not {arm.type}")
    if arm2.type != 'ARMATURE':
        raise Exception(f"{proportions_name} must be an ARMATURE, not {arm2.type}")
    
    # Duplicate imported armature (data-only)
    new_arm_data = arm.data.copy()
    new_arm_obj = arm.copy()
    new_arm_obj.data = new_arm_data
    bpy.context.collection.objects.link(new_arm_obj)
    
    # Enter edit mode on proportions armature
    prev_mode = arm2.mode
    bpy.context.view_layer.objects.active = arm2
    arm2.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    
    arm2_eb = arm2.data.edit_bones
    new_eb = new_arm_obj.data.edit_bones
    
    # Merge non-ValveBiped bones
    for bone in new_eb:
        if bone.name not in VALVEBIPED_BONES:
            b = arm2_eb.new(bone.name)
            b.head = bone.head.copy()
            b.tail = bone.tail.copy()
            b.roll = bone.roll
            
            pname = bone.parent.name if bone.parent else 'ValveBiped.Bip01_Pelvis'
            if pname in arm2_eb:
                b.parent = arm2_eb[pname]
    
    # Return to previous mode
    bpy.ops.object.mode_set(mode=prev_mode)
    
    # Remove temporary duplicate armature
    bpy.data.objects.remove(new_arm_obj, do_unlink=True)
    
    # Update armature modifiers on all meshes
    for ob in bpy.context.scene.objects:
        if ob.type == 'MESH':
            arm_mod = next((m for m in ob.modifiers if m.type == 'ARMATURE'), None)
            if arm_mod:
                arm_mod.object = arm2
            else:
                mod = ob.modifiers.new('Armature', 'ARMATURE')
                mod.object = arm2


def make_toe_vertical(bone) -> None:
    """
    Adjust toe bone to be vertical.
    
    Args:
        bone: The edit bone to adjust
    """
    if bone:
        print(f"Making toe vertical: {bone.name}")
        bone.tail.x = bone.head.x
        bone.tail.y = bone.head.y


def clear_pose_bone_constraints(bone, armature) -> None:
    """
    Remove all constraints from a pose bone.
    
    Args:
        bone: The pose bone to clear
        armature: The armature object (must be in POSE mode)
    """
    if armature.mode != "POSE":
        raise Exception('Object Mode not Pose Mode.')
    
    for constraint in bone.constraints:
        bone.constraints.remove(constraint)
