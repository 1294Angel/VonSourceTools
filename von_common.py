#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Import Bullshit

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import bpy # type: ignore
from pathlib import Path







#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Common Functions

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def reselect_all(objectsToSelect:list, targetobj):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objectsToSelect:
        o.select_set(True)
    bpy.context.view_layer.objects.active = targetobj
    

def move_object_to_collection(objName:str, targetCollection:str):
    if targetCollection in bpy.data.collections:
        targetCollection = bpy.data.collections[targetCollection]
    else:
        targetCollection = bpy.data.collections.new(targetCollection)
        bpy.context.scene.collection.children.link(targetCollection)

    obj = bpy.data.objects.get(objName)

    if obj:
        for coll in obj.users_collection:
            coll.objects.unlink(obj)
        
        targetCollection.objects.link(obj)
    else:
            print(f"Object {objName} not found")

def object_exists(name: str) -> bool:
    doesExist = False
    obj = bpy.data.objects.get(name)
    if obj:
        doesExist = True
    return doesExist

def importitemfromdict(name:str, collection:str, targetdict:dict):
    filepath: str = ""
    try:
        bpy.ops.import_scene.fbx(filepath=str(targetdict[name]))
    except:
        raise ImportError(f"Object {name} not found")
    move_object_to_collection(name, collection)

def set_object_mode(obj, mode:str="OBJECT"):
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.mode_set(mode=mode)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Delta Anim Data Storage

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def deltaanimtrick_valvebipeds_1():
    valvebipeds = [
    'ValveBiped.Bip01_Pelvis',
    'ValveBiped.Bip01_Spine',
    'ValveBiped.Bip01_Spine1',
    'ValveBiped.Bip01_Spine2',
    'ValveBiped.Bip01_Spine4',
    'ValveBiped.Bip01_Neck1',
    'ValveBiped.Bip01_Head1',
    'ValveBiped.Bip01_R_Clavicle',
    'ValveBiped.Bip01_R_UpperArm',
    'ValveBiped.Bip01_R_Forearm',
    'ValveBiped.Bip01_R_Hand',
    'ValveBiped.Bip01_R_Finger0',
    'ValveBiped.Bip01_R_Finger01',
    'ValveBiped.Bip01_R_Finger02',
    'ValveBiped.Bip01_R_Finger1',
    'ValveBiped.Bip01_R_Finger11',
    'ValveBiped.Bip01_R_Finger12',
    'ValveBiped.Bip01_R_Finger2',
    'ValveBiped.Bip01_R_Finger21',
    'ValveBiped.Bip01_R_Finger22',
    'ValveBiped.Bip01_R_Finger3',
    'ValveBiped.Bip01_R_Finger31',
    'ValveBiped.Bip01_R_Finger32',
    'ValveBiped.Bip01_R_Finger4',
    'ValveBiped.Bip01_R_Finger41',
    'ValveBiped.Bip01_R_Finger42',
    'ValveBiped.Bip01_L_Clavicle',
    'ValveBiped.Bip01_L_UpperArm',
    'ValveBiped.Bip01_L_Forearm',
    'ValveBiped.Bip01_L_Hand',
    'ValveBiped.Bip01_L_Finger0',
    'ValveBiped.Bip01_L_Finger01',
    'ValveBiped.Bip01_L_Finger02',
    'ValveBiped.Bip01_L_Finger1',
    'ValveBiped.Bip01_L_Finger11',
    'ValveBiped.Bip01_L_Finger12',
    'ValveBiped.Bip01_L_Finger2',
    'ValveBiped.Bip01_L_Finger21',
    'ValveBiped.Bip01_L_Finger22',
    'ValveBiped.Bip01_L_Finger3',
    'ValveBiped.Bip01_L_Finger31',
    'ValveBiped.Bip01_L_Finger32',
    'ValveBiped.Bip01_L_Finger4',
    'ValveBiped.Bip01_L_Finger41',
    'ValveBiped.Bip01_L_Finger42',
    'ValveBiped.Bip01_R_Thigh',
    'ValveBiped.Bip01_R_Calf',
    'ValveBiped.Bip01_R_Foot',
    'ValveBiped.Bip01_R_Toe0',
    'ValveBiped.Bip01_L_Thigh',
    'ValveBiped.Bip01_L_Calf',
    'ValveBiped.Bip01_L_Foot',
    'ValveBiped.Bip01_L_Toe0',
    ]

    return valvebipeds


def deltaanimtrick_valvebipeds_2():
    valvebipeds2 = [
    'ValveBiped.Bip01_L_Thigh',
    'ValveBiped.Bip01_L_Calf',
    'ValveBiped.Bip01_L_Calf',
    'ValveBiped.Bip01_L_Foot',
    'ValveBiped.Bip01_R_Thigh',
    'ValveBiped.Bip01_R_Calf',
    'ValveBiped.Bip01_R_Calf',
    'ValveBiped.Bip01_R_Foot',
    'ValveBiped.Bip01_L_UpperArm',
    'ValveBiped.Bip01_L_Forearm',
    'ValveBiped.Bip01_L_Forearm',
    'ValveBiped.Bip01_L_Hand',
    'ValveBiped.Bip01_R_UpperArm',
    'ValveBiped.Bip01_R_Forearm',
    'ValveBiped.Bip01_R_Forearm',
    'ValveBiped.Bip01_R_Hand',
    'ValveBiped.Bip01_L_Finger0',
    'ValveBiped.Bip01_L_Finger01',
    'ValveBiped.Bip01_L_Finger01',
    'ValveBiped.Bip01_L_Finger02',
    'ValveBiped.Bip01_L_Finger1',
    'ValveBiped.Bip01_L_Finger11',
    'ValveBiped.Bip01_L_Finger11',
    'ValveBiped.Bip01_L_Finger12',
    'ValveBiped.Bip01_L_Finger2',
    'ValveBiped.Bip01_L_Finger21',
    'ValveBiped.Bip01_L_Finger21',
    'ValveBiped.Bip01_L_Finger22',
    'ValveBiped.Bip01_L_Finger3',
    'ValveBiped.Bip01_L_Finger31',
    'ValveBiped.Bip01_L_Finger31',
    'ValveBiped.Bip01_L_Finger32',
    'ValveBiped.Bip01_L_Finger4',
    'ValveBiped.Bip01_L_Finger41',
    'ValveBiped.Bip01_L_Finger41',
    'ValveBiped.Bip01_L_Finger42',
    'ValveBiped.Bip01_R_Finger0',
    'ValveBiped.Bip01_R_Finger01',
    'ValveBiped.Bip01_R_Finger01',
    'ValveBiped.Bip01_R_Finger02',
    'ValveBiped.Bip01_R_Finger1',
    'ValveBiped.Bip01_R_Finger11',
    'ValveBiped.Bip01_R_Finger11',
    'ValveBiped.Bip01_R_Finger12',
    'ValveBiped.Bip01_R_Finger2',
    'ValveBiped.Bip01_R_Finger21',
    'ValveBiped.Bip01_R_Finger21',
    'ValveBiped.Bip01_R_Finger22',
    'ValveBiped.Bip01_R_Finger3',
    'ValveBiped.Bip01_R_Finger31',
    'ValveBiped.Bip01_R_Finger31',
    'ValveBiped.Bip01_R_Finger32',
    'ValveBiped.Bip01_R_Finger4',
    'ValveBiped.Bip01_R_Finger41',
    'ValveBiped.Bip01_R_Finger41',
    'ValveBiped.Bip01_R_Finger42',
    ]

    return valvebipeds2

def deltaanimtrick_armaturefilelocations():
    print("---------Running Delta Anim Armature File Locations Definition ----------")
    base_dir = Path(__file__).parent / "storeditems" / "deltaanimtrick"
    armaturelocations = {
        "proportions": base_dir / "proportions.fbx",
        "reference_female": base_dir / "reference_female.fbx",
        "reference_male": base_dir / "reference_male.fbx"
    }
    return armaturelocations


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # QC Data Storage

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def qc_types():
    qcDefaults = {
        "PROP": {
            "flags": ["$staticprop"],
            "sections": ["$modelname", "$cdmaterials", "$body", "$sequence", "$collisionmodel"]
        },
        "CHARACTER": {
            "flags": [],
            "sections": ["$modelname", "$cdmaterials", "$body", "$sequence", "$collisionmodel", "$attachment"]
        },
        "NPC": {
            "flags": [],
            "sections": ["$modelname", "$cdmaterials", "$body", "$sequence", "$collisionmodel", "$surfaceprop"]
        }
    }
    return qcDefaults

def qc_populate_typesEnum(qcDefaults):
    enumItems = []
    for dict in qcDefaults:
        enumItems.append((dict,dict,f"Select if your QC is going to be: {dict}"))
    return enumItems

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Inter-File Storage

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class VonData(bpy.types.PropertyGroup):



    #---------------------------------------------------------------- Delta Anim Stuff
    float_deltaAnim_simmilarityThreshold : bpy.props.FloatProperty(
        name="Simmilarity Threshhold",
        description="Percentage of bones need to match the default valve biped armature in order to be valid.",
        default=90.0,
        min=0.0, max=100.0,
        soft_min=0.0, soft_max=100.0,
        step=1.0,
    ) # type: ignore



    #---------------------------------------------------------------- QC Generator Stuff

    enum_qcGen_modelType : bpy.props.EnumProperty(
        name="QC Type",
        description="Type of model you're making a QC for, is it a prop, character, npc?",
        items=  qc_populate_typesEnum(qc_types())
    ) # type: ignore

    string_qcGen_outputPath : bpy.props.StringProperty(
        name="Output Filepath",
        description="Filepath the created QC file will output to",
        default = str(Path(__file__).parent),
        subtype='FILE_PATH'
    ) # type: ignore

    string_qcGen_materialPath : bpy.props.StringProperty(
        name="Material Subfolder Filepath",
        description="Filepath after the material's folder where the VMT files will be located.",
        default = "",
        subtype='FILE_PATH'
    ) # type: ignore

    bool_qcGen_scale : bpy.props.IntProperty(
        name = "Character Scale",
        description = "Scale of the characeter",
        default = 1,
        soft_min = 0,
        soft_max = 10,
        step = 1
    ) # type: ignore

    bool_qcGen_generateCollission : bpy.props.BoolProperty(
        name = "Generate Collisions?",
        description = "Should Collisions be automatically generated?",
        default = False
    ) # type: ignore

    string_qcGen_existingCollissionCollection : bpy.props.StringProperty(
        name="Existing Collission Collection",
        description="Name of the existing collission mesh collection",
        default = "",
    ) # type: ignore







#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Register Functions

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
classes = [
    #Random Storage Classes

    #Pointer Property
    VonData
]

def von_common_register():
    from bpy.utils import register_class # type: ignore
    for cls in classes:
        register_class(cls)    
    bpy.types.Scene.toolBox = bpy.props.PointerProperty(type=VonData)

def von_common_unregister():
    from bpy.utils import unregister_class # type: ignore
    for cls in classes:
        unregister_class(cls)    
    del bpy.types.Scene.toolBox