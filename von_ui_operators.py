import bpy # type: ignore
from . import von_deltaanimtrick
from . import von_common

#-------------------------------------------------------------------------------------------------------------------------------------------------
# Delta Anim Trick
#-------------------------------------------------

def hasproperties():
    hasproportions = bpy.data.objects.get("proportions")
    hasmaleref = bpy.data.objects.get("reference_female")
    hasfemaleref = bpy.data.objects.get("reference_male")

    if hasproportions:
        for col in hasproportions.users_collection:
            col.objects.unlink(hasproportions)
        bpy.data.objects.remove(hasproportions)
        von_common.importitemfromdict("proportions", "Collection 2", von_common.deltaanimtrick_armaturefilelocations())
        hasproportions = True
    else:
        von_common.importitemfromdict("proportions", "Collection 2", von_common.deltaanimtrick_armaturefilelocations())
        hasproportions = True
    if not hasfemaleref:
        von_common.importitemfromdict("reference_female", "Collection 3", von_common.deltaanimtrick_armaturefilelocations())
        hasfemaleref = True
    if not hasmaleref:
        von_common.importitemfromdict("reference_male", "Collection 3", von_common.deltaanimtrick_armaturefilelocations())
        hasmaleref = True
    return hasproportions, hasmaleref, hasfemaleref

class Vonpanel_DeltaAnimTrick_ImportRequiredProperties(bpy.types.Operator):
    bl_idname = "von.deltaanimtrick_importrequiredproperties"
    bl_label = "Import Required Armatures"
    def execute(self,context):
        hasproportions, hasmaleref, hasfemaleref = hasproperties()
        try:
            print(f"hasproportions = {hasproportions} ||| hasmaleref = {hasmaleref} ||| hasfemaleref = {hasfemaleref}")
        except:
            return{'ERROR'}
        return{'FINISHED'}


class VonPanel_DeltaAnimTrick_PartOne(bpy.types.Operator):
    bl_idname = "von.deltaanimtrick_partone"
    bl_label = "Delta Anim Trick (One)"
    def execute(self, context):
        #Import reference armatures
        hasproportions: bool = False
        hasmaleref: bool = False
        hasfemaleref: bool = False

        hasproportions, hasmaleref, hasfemaleref = hasproperties()

        if hasproportions and hasmaleref and hasfemaleref == True:
            #Get selected armatures
            obj = [obj for obj in bpy.data.objects if object.type == "ARMATURE"]
            #Run once on each valid armature
            for armature in obj:
                von_deltaanimtrick.delta_anim_trick_one(armature)
            return{"FINISHED"}
        return{'ERROR'}

class VonPanel_DeltaAnimTrick_PartTwo(bpy.types.Operator):
    bl_idname = "von.deltaanimtrick_parttwo"
    bl_label = "Delta Anim Trick (Two)"
    def execute(self, context):
        #Import reference armatures
        hasproportions: bool = False
        hasmaleref: bool = False
        hasfemaleref: bool = False
        hasproportions, hasmaleref, hasfemaleref = hasproperties()

        if hasproportions and hasmaleref and hasfemaleref == True:
            #Get selected armatures
            obj = [obj for obj in bpy.data.objects if object.type == "ARMATURE"]
            #Run once on each valid armature
            for armature in obj:
                von_deltaanimtrick.delta_anim_trick_two(armature)
            return{"FINISHED"}
        return{'ERROR'}

class VonPanel_DeltaAnimTrick_Full(bpy.types.Operator):
    bl_idname = "von.deltaanimtrick_full"
    bl_label = "Delta Anim Trick (Full)"
        

    def execute(self, context):


        originalviewmode = bpy.context.active_object

        #Import reference armatures
        hasproportions: bool = False
        hasmaleref: bool = False
        hasfemaleref: bool = False
        hasproportions, hasmaleref, hasfemaleref = hasproperties()

        if hasproportions and hasmaleref and hasfemaleref == True:
            
        
            #Get selected armatures
            obj = [obj for obj in bpy.data.objects if object.type == "ARMATURE"]
            #Run once on each valid armature
            for armature in obj:
                editbones = armature.edit_bones
                posebones = armature.pose.bones

                von_deltaanimtrick.delta_anim_trick_one(armature)

                bpy.ops.object.mode_set(mode='EDIT')
                for bone in editbones:
                    von_deltaanimtrick.toevertical(bone)
            
                bpy.ops.object.mode_set(mode='POSE')
                bpy.ops.pose.armature_apply(selected=False)

                for bone in posebones:
                    von_deltaanimtrick.clearposeboneconstraints(bone)
                
                von_deltaanimtrick.delta_anim_trick_two(armature)

            bpy.ops.object.mode_set(mode=originalviewmode)
            return{"FINISHED"}
        return{'ERROR'}

#-------------------------------------------------------------------------------------------------------------------------------------------------
# SMD Exporter Script
#-------------------------------------------------



# ----------------------------------------------------------------------------------------------------------------------------------------------------
# Register Fnction
# ----------------------------


classes = (
    Vonpanel_DeltaAnimTrick_ImportRequiredProperties,
    VonPanel_DeltaAnimTrick_PartOne,
    VonPanel_DeltaAnimTrick_PartTwo,
    VonPanel_DeltaAnimTrick_Full
)


def von_operator_register():
    for cls in classes:
        bpy.utils.register_class(cls)    


def von_operator_unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)