import bpy # type: ignore
from collections import OrderedDict
from . import von_common






#-------------------------------------------------------------------------------------------------------------

def delta_anim_trick_one(sourceArmature: bpy.types.Object):
    if 'proportions' not in bpy.data.objects:
        raise Exception("No armature named 'proportions' found in the scene.")
    targetArmature = bpy.data.objects['proportions']

    if targetArmature.type != 'ARMATURE':
        raise TypeError(f"Target armature 'proportions' must be an ARMATURE, not {targetArmature.type}")
    if sourceArmature.type != 'ARMATURE':
        raise TypeError(f"Source armature must be an ARMATURE, not {sourceArmature.type}")

    valvebipeds = von_common.deltaanimtrick_valvebipeds_1()

    valvebipeds2 = von_common.deltaanimtrick_valvebipeds_2()

    targetBones = valvebipeds2[::2]
    subBones = valvebipeds2[1::2]
    d = OrderedDict()
    for idx, value in enumerate(subBones):
        d[f'var{idx}'] = value

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
        c1.subtarget = d[f'var{idx}']
        c1.track_axis = 'TRACK_X'
        c1.lock_axis = 'LOCK_Z'

        c2 = targetBone.new('LOCKED_TRACK')
        c2.name = 'Locked Track_XY'
        c2.target = sourceArmature
        c2.subtarget = d[f'var{idx}']
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



def delta_anim_trick_two(arm):
    print("---------Running Delta Anim Trick Two Definition ----------")
    arm2 = bpy.data.objects['proportions']
    objects = bpy.context.scene.objects

    valvebipeds = von_common.deltaanimtrick_valvebipeds_1()

    bn = []
    pr = []

    bpy.data.objects['proportions'].hide_set(True)
    bpy.data.objects[arm.name].hide_set(False)
    bpy.context.view_layer.objects.active = bpy.data.objects[arm.name]
    bpy.data.objects[arm.name].select_set(True)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.duplicate()
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.select_all(action='DESELECT')

    for bone in bpy.context.object.data.edit_bones:
        if bone.name in valvebipeds:
            bone.select = True
            bone.select_head = True
            bone.select_tail = True

    bpy.ops.armature.delete()
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.objects['proportions'].hide_set(False)
    bpy.data.objects[arm.name].hide_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects['proportions']
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.join()
    bpy.ops.object.mode_set(mode='EDIT')

    for bone in arm.data.bones:
        if bone.name not in valvebipeds:
            bn.append(bone.name)

    for bone in arm.data.bones:
        if bone.name not in valvebipeds:
            pr.append(getattr(bone.parent, 'name', 'ValveBiped.Bip01_Pelvis'))

    for bone in bpy.context.object.data.edit_bones:
        j = 0    
        i = 0
        while j < len(bn) and i < len(pr):
            arm2.data.edit_bones[bn[i]].parent = arm2.data.edit_bones[pr[j]]
            j += 1        
            i += 1
            
    bpy.ops.object.mode_set(mode='OBJECT')

    #add armature modifier
    for ob in objects:
        if ob.type == 'MESH':
            if ob.modifiers.values() == []:
                ob.modifiers.new('Armature_01', 'ARMATURE')
                ob.modifiers['Armature'].object = bpy.data.objects['proportions']
            else:
                for mods in ob.modifiers.values():
                    if mods.name == 'Armature':
                        ob.modifiers['Armature'].object = bpy.data.objects['proportions']
                    else:
                        ob.modifiers.new('Armature_01', 'ARMATURE')
                        ob.modifiers['Armature'].object = bpy.data.objects['proportions']
    


#-------------------------------------------------------------------------------------------------------------

def toevertical(bone):
    print("---------Running Delta Anim Trick Toe Vertical Definition ----------")
    object = bpy.context.active_object
    if object.mode == "EDIT":
        raise Exception('Object Mode not Edit Mode.')
    
    bone.tail.x = bone.head.x
    bone.tail.y = bone.head.y




def clearposeboneconstraints(bone):
    print("---------Running Delta Anim Trick Clear Pose Definition ----------")
    object = bpy.context.active_object
    if object.mode != "POSE":
        raise Exception('Object Mode not Pose Mode.')
    for constraint in bone.constraints:
        if constraint.type == "COPY_LOCATION":
            bone.constraints.remove(constraint)