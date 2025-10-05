import bpy # type: ignore
from collections import OrderedDict
from . import von_common






#-------------------------------------------------------------------------------------------------------------
def delta_anim_trick_one(armature):
    valvebipeds = von_common.deltaanimtrick_valvebipeds_1()
    valvebipeds2 = von_common.deltaanimtrick_valvebipeds_2()

    target = valvebipeds2[::2]
    sub = valvebipeds2[1::2]

    d = OrderedDict()
    for i, value in enumerate(sub):
        key = 'var' + str(i)
        d[key] = value 
        
    for i in valvebipeds:
        objbone = bpy.data.objects['proportions'].pose.bones[i].constraints
        
        if armature.pose.bones.get(i) is not None:
            objbone.new('COPY_LOCATION')
            objbone['Copy Location'].target = armature
            objbone['Copy Location'].subtarget = i

    for j, k in enumerate(target):
        objbone2 = bpy.data.objects['proportions'].pose.bones[k].constraints
        
        if armature.pose.bones.get(k) is not None:
            objbone2.new('LOCKED_TRACK')
            objbone2['Locked Track'].target = armature
            objbone2['Locked Track'].subtarget = d["var"+str(j)]
            objbone2['Locked Track'].track_axis = 'TRACK_X'
            objbone2['Locked Track'].lock_axis = 'LOCK_Z'
            objbone2.new('LOCKED_TRACK')
            objbone2['Locked Track.001'].target = armature
            objbone2['Locked Track.001'].subtarget = d["var"+str(j)]
            objbone2['Locked Track.001'].track_axis = 'TRACK_X'
            objbone2['Locked Track.001'].lock_axis = 'LOCK_Y'

    #removes LOCKED_TRACK on parent if child constraint is empty			
    for l in valvebipeds:
        objbone3 = bpy.data.objects['proportions'].pose.bones[l]
            
        for child in objbone3.children:    
            objbone4 = bpy.data.objects['proportions'].pose.bones[child.name].constraints
            
            if not objbone4.keys():
                if objbone3.parent is not None:
                    objbone5 = bpy.data.objects['proportions'].pose.bones[l].constraints
                    
                    for constraint in objbone5:
                        if constraint.name != 'Copy Location':
                            objbone5.remove(constraint)
        
            print(l+' is a parent of '+child.name+' with constraint: ',objbone3.constraints.keys())
            
    bpy.data.objects['proportions'].hide_set(False)
    bpy.data.objects[armature.name].hide_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects['proportions']
    bpy.data.objects['proportions'].select_set(True)
    bpy.ops.object.mode_set(mode='POSE')


def delta_anim_trick_two(arm):
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
    object = bpy.context.active_object
    if object.mode == "EDIT":
        raise Exception('Object Mode not Edit Mode.')
    
    bone.tail.x = bone.head.x
    bone.tail.y = bone.head.y




def clearposeboneconstraints(bone):
    object = bpy.context.active_object
    if object.mode == "POSE":
        raise Exception('Object Mode not Pose Mode.')
    for constraint in bone.constraints:
        if constraint.type == "COPY_LOCATION":
            bone.constraints.remove(constraint)