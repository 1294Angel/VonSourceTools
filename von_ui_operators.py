import bpy # type: ignore
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
def qcoptions(context):
     scene = context.scene
     data = {
        "modelType": scene.qc_model_type,                # PROP / CHARACTER / NPC
        "modelName": scene.qc_model_name,                # "cratestack"
        "outputPath": bpy.path.abspath(scene.qc_output_path),
        "cdMaterials": scene.qc_material_path,           # e.g. "models/props/"
        "smdPath": scene.qc_smd_path,                    # e.g. "//exports/cratestack.smd"
        "collisionModel": scene.qc_collision_path,       # e.g. "//exports/cratestack_phys.smd"
        "scale": scene.qc_scale,                         # numeric, e.g. 1.0
        "bodygroup": scene.qc_bodygroup or "Body",
        "surfaceProp": scene.qc_surfaceprop or "metal",
        "staticProp": scene.qc_staticprop,               # bool
        "sequenceName": scene.qc_sequence or "idle",     # for characters/NPCs
    }

class qcgenerator():
    print("Running QC Generator")

    #Get location of VMT file
    #Get all materials on object
    #Get optionals


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