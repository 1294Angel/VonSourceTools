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

def qc_file_types(): #Remember to add any additions to the UI as well - Otherwise they will not appear
    qcDefaults = {
        "PROP": {
            "flags": ["$staticprop"],
            "sections": ["$modelname", "$cdmaterials", "$bodygroup", "$sequence", "$collisionmodel"]
        },
        "CHARACTER": {
            "flags": [],
            "sections": ["$modelname", "$cdmaterials", "$bodygroup", "$sequence", "$collisionmodel", "$attachment"]
        },
        "NPC": {
            "flags": [],
            "sections": ["$modelname", "$cdmaterials", "$bodygroup", "$sequence", "$collisionmodel", "$surfaceprop"]
        }
    }
    return qcDefaults

def qc_populate_typesEnum(qcDefaults):
    enumItems = []
    for dict in qcDefaults:
        enumItems.append((dict,dict,f"Select if your QC is going to be: {dict}"))
    return enumItems

#storage for collections in scene
class QC_BodygroupCollectionItem(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty() # type: ignore
    enabled : bpy.props.BoolProperty(
        name="Include", 
        default=False
        ) # type: ignore

class QC_BodygroupBox(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(
        name="Bodygroup Name", 
        default="New Bodygroup"
        ) # type: ignore
    collections : bpy.props.CollectionProperty(type=QC_BodygroupCollectionItem) # type: ignore

class QC_PrimaryData(bpy.types.PropertyGroup):
    num_boxes : bpy.props.IntProperty(
        name="Number of Boxes", 
        default=1, 
        min=1
        ) # type: ignore
    bodygroup_boxes : bpy.props.CollectionProperty(type=QC_BodygroupBox) # type: ignore
def sync_bodygroup_boxes(scene):
    qcData = scene.QC_PrimaryData
    existing_collections = [col.name for col in bpy.data.collections]

    # Ensure enough boxes
    while len(qcData.bodygroup_boxes) < qcData.num_boxes:
        qcData.bodygroup_boxes.add()

    while len(qcData.bodygroup_boxes) > qcData.num_boxes:
        qcData.bodygroup_boxes.remove(len(qcData.bodygroup_boxes)-1)

    # Ensure each box has all collections
    for box in qcData.bodygroup_boxes:
        existing_names = {item.name for item in box.collections}
        for name in existing_collections:
            if name not in existing_names:
                item = box.collections.add()
                item.name = name
                item.enabled = False  # default
def get_bodygroup_by_name(qcData, box_name):
    for box in qcData.bodygroup_boxes:
        if box.name == box_name:
            return box
    return None


def QC_Get_Specific_Collection_From_Refreshed_List(collectionToGet:str = ""):
    qcData = bpy.context.scene.QC_PrimaryData
    enabled = False

    for item in qcData.qc_collections:
        if item.name == collectionToGet:
            enabled = item.enabled
            break
    return enabled

#Get submeshes of each bodygroup
def QC_Get_SubMeshes_Of_Box():
    retData = {}
    qcData = bpy.context.scene.QC_PrimaryData
    head_box = get_bodygroup_by_name(qcData, "Head")

    if head_box:
        for item in head_box.collections:
            print(item.name, item.enabled)

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
        items=  qc_populate_typesEnum(qc_file_types())
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

    int_qcGen_scale : bpy.props.IntProperty(
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

    string_qcGen_mdlModelName : bpy.props.StringProperty(
        name="Name of the compiled Model",
        description="Final name of the compiled asset",
        default = "",
    ) # type: ignore







#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Register Functions

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
classes = [
    #QC Classes:
    QC_BodygroupCollectionItem,
    QC_BodygroupBox,
    QC_PrimaryData,
    #Pointer Property
    VonData
]

pointerproperties = [
    VonData,
    QC_PrimaryData
]

def von_common_register():
    from bpy.utils import register_class # type: ignore
    for cls in classes:
        register_class(cls)    
    bpy.types.Scene.toolBox = bpy.props.PointerProperty(type=VonData)
    bpy.types.Scene.QC_PrimaryData = bpy.props.PointerProperty(type=QC_PrimaryData)


def von_common_unregister():
    from bpy.utils import unregister_class # type: ignore
    for cls in classes:
        unregister_class(cls)    
    del bpy.types.Scene.toolBox
    del bpy.types.Scene.QC_PrimaryData