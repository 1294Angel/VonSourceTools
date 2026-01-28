import bpy # type: ignore
from collections import OrderedDict
from . import von_common




# README -- All code from here is not mine, I've taken code from: https://github.com/sksh70/proportion_trick_script -- All I have done is modify the base code from 2.9 to create functionality and added some functions to automate certain steps.

#-------------------------------------------------------------------------------------------------------------



def delta_anim_trick_one(sourceArmature: bpy.types.Object):
    if 'proportions' not in bpy.data.objects:
        raise Exception("No armature named 'proportions' found in the scene.")
    targetArmature = bpy.data.objects['proportions']
    if isinstance(sourceArmature, str):
        bpy.data.objects[sourceArmature]

    if targetArmature.type != 'ARMATURE':
        raise TypeError(f"Target armature 'proportions' must be an ARMATURE, not {targetArmature.type}")
    if sourceArmature.type != 'ARMATURE':
        raise TypeError(f"Source armature must be an ARMATURE, not {sourceArmature.type}")

    valvebipeds = von_common.deltaanimtrick_valvebipeds_1()

    valvebipeds2 = von_common.deltaanimtrick_valvebipeds_2()
    targetBones = valvebipeds2[::2]
    subBones = valvebipeds2[1::2]
    bone_mapping = OrderedDict()
    for idx, value in enumerate(subBones):
        bone_mapping[f'var{idx}'] = value

    for boneName in valvebipeds:
        if boneName not in targetArmature.pose.bones:
            continue
        targetBone = targetArmature.pose.bones[boneName].constraints

        if 'Copy Location' not in targetBone:
            c = targetBone.new('COPY_LOCATION')
            c.name = 'Copy Location'
            c.target = sourceArmature
            c.subtarget = boneName

    for idx, boneName in enumerate(targetBones):
        if boneName not in targetArmature.pose.bones:
            continue
        targetBone = targetArmature.pose.bones[boneName].constraints

        c1 = targetBone.new('LOCKED_TRACK')
        c1.name = 'Locked Track_XZ'
        c1.target = sourceArmature
        c1.subtarget = bone_mapping[f'var{idx}']
        c1.track_axis = 'TRACK_X'
        c1.lock_axis = 'LOCK_Z'

        c2 = targetBone.new('LOCKED_TRACK')
        c2.name = 'Locked Track_XY'
        c2.target = sourceArmature
        c2.subtarget = bone_mapping[f'var{idx}']
        c2.track_axis = 'TRACK_X'
        c2.lock_axis = 'LOCK_Y'

    for boneName in valvebipeds:
        if boneName not in targetArmature.pose.bones:
            continue
        parentBone = targetArmature.pose.bones[boneName]

        for child in parentBone.children:
            childConstraints = targetArmature.pose.bones[child.name].constraints
            if not childConstraints.keys():
                for constraint in parentBone.constraints:
                    if constraint.type != 'COPY_LOCATION':
                        parentBone.constraints.remove(constraint)

    targetArmature.hide_set(False)
    sourceArmature.hide_set(True)
    bpy.context.view_layer.objects.active = targetArmature
    targetArmature.select_set(True)
    bpy.ops.object.mode_set(mode='POSE')

    print(f"'proportions' aligned to {sourceArmature.name} successfully!")

def delta_anim_trick_two(imported_name="gg", proportions_name="proportions"):

    # --- Safety checks ---
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

    # --- Get ValveBiped bones list ---
    valvebipeds = von_common.deltaanimtrick_valvebipeds_1()

    # --- Duplicate imported armature (data-only, no ops) ---
    new_arm_data = arm.data.copy()
    new_arm_obj = arm.copy()
    new_arm_obj.data = new_arm_data
    bpy.context.collection.objects.link(new_arm_obj)

    # --- Enter edit mode on proportions armature ---
    prev_mode:str = arm2.mode
    bpy.context.view_layer.objects.active = arm2
    arm2.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')

    arm2_eb = arm2.data.edit_bones
    new_eb = new_arm_obj.data.edit_bones

    # --- Merge non-ValveBiped bones ---
    for bone in new_eb:
        if bone.name not in valvebipeds:
            # Copy bone into arm2
            b = arm2_eb.new(bone.name)
            b.head = bone.head.copy()
            b.tail = bone.tail.copy()
            b.roll = bone.roll

            # Parent the bone
            pname = bone.parent.name if bone.parent else 'ValveBiped.Bip01_Pelvis'
            if pname in arm2_eb:
                b.parent = arm2_eb[pname]

    # --- Return proportions armature to previous mode ---
    bpy.ops.object.mode_set(mode=prev_mode)

    # --- Remove temporary duplicate armature ---
    bpy.data.objects.remove(new_arm_obj, do_unlink=True)

    # --- Add or update armature modifier on all meshes ---
    for ob in bpy.context.scene.objects:
        if ob.type == 'MESH':
            arm_mod = next((m for m in ob.modifiers if m.type == 'ARMATURE'), None)
            if arm_mod:
                arm_mod.object = arm2
            else:
                mod = ob.modifiers.new('Armature', 'ARMATURE')
                mod.object = arm2










    


#-------------------------------------------------------------------------------------------------------------

def toevertical(bone):
    if bone:
        print("---------Running Delta Anim Trick Toe Vertical Definition ----------")
        print(bone.name)
        bone.tail.x = bone.head.x
        bone.tail.y = bone.head.y




def clearposeboneconstraints(bone, armature):
    print("---------Running Delta Anim Trick Clear Pose Constraints Definition ----------")
    if armature.mode != "POSE":
        raise Exception('Object Mode not Pose Mode.')
    for constraint in bone.constraints:
        bone.constraints.remove(constraint)