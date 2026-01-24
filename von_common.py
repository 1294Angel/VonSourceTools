import bpy,json# type: ignore
from pathlib import Path
##----------------------------------------------------------------------
# Harded Coded File Locs
#----------------------------------------------------------------------
default_surfaceprop_path = str(Path(__file__).parent / "storeditems" / "qcgenerator" / "templates" / "surfaceprops.json")

MODEL_TYPE_CATEGORY_MAP = {
    "NPC": [
        "Basic", "Movement", "Combat", "Gestures",
        "NPC_Reactions", "Signals_Commands", "Interaction",
        "Swimming", "Vehicles", "Scripted_Sequences"
    ],
    "CHARACTER": [
        "Basic", "Movement", "Combat", "Gestures",
        "NPC_Reactions", "Signals_Commands", "Interaction",
        "Swimming", "Vehicles", "Scripted_Sequences"
    ],
    "VIEWMODEL": ["Viewmodel"],
    "PROP": [],
    "WORLDMODEL": []
}
NONE_ENUM = ("NONE", "None", "")
#----------------------------------------------------------------------
    # Delta Anim Data Storage
#----------------------------------------------------------------------

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

    base_dir = Path(__file__).parent / "storeditems" / "deltaanimtrick"
    armaturelocations = {
        "proportions": base_dir / "proportions.fbx",
        "reference_female": base_dir / "reference_female.fbx",
        "reference_male": base_dir / "reference_male.fbx"
    }
    return armaturelocations


#----------------------------------------------------------------------
# Commonly Used Functions
#----------------------------------------------------------------------

def load_json_dict_to_var(relativePath: str, jsonFileName) -> dict:
    addonDir = Path(__file__).parent
    jsonPath = addonDir / relativePath / jsonFileName

    if not jsonPath.isfile():
        raise FileNotFoundError(f"Json Dict not found: {jsonPath}")
    with jsonPath.open("r", encoding="utf-8") as f:
        data = json.load(f)
    
    return data
def reselect_all(objectsToSelect:list, targetobj):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objectsToSelect:
        o.select_set(True)
    bpy.context.view_layer.objects.active = targetobj

def move_object_to_collection(objName:str, targetCollection:str):
    print(targetCollection)
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
    print(f"IMPORT FROM DICT ------- collection = {collection}")
    filepath: str = ""
    try:
        bpy.ops.import_scene.fbx(filepath=str(targetdict[name]))
    except:
        raise ImportError(f"Object {name} not found")
    move_object_to_collection(name, collection)

#----------------------------------------------------------------------
# BoneLoc For QC $Attachment Storage
#----------------------------------------------------------------------

class Bone_NameForAttach(bpy.types.PropertyGroup):
    bonename: bpy.props.StringProperty(
        name="Bone Name"
    ) # type: ignore

class Armature_Name(bpy.types.PropertyGroup):
    armatureName: bpy.props.StringProperty(
        name="Armature"
    ) # type: ignore
    sequences: bpy.props.CollectionProperty(type=Bone_NameForAttach)  # type: ignore

#----------------------------------------------------------------------
# VMT Filepath Storage
#----------------------------------------------------------------------

class VMT_FilePathItem(bpy.types.PropertyGroup):
    filepath: bpy.props.StringProperty(
        name="File Path",
        subtype='FILE_PATH'
    ) # type: ignore

#----------------------------------------------------------------------
# Animation Sequence Filepath Storage
#----------------------------------------------------------------------

def activity_item_items(self, context):
    NONE_ENUM = ("NONE", "None", "Do not replace any activity")

    toolbox = context.scene.toolBox
    json_path = Path(toolbox.string_activityfilelocation)
    if not json_path.is_file():
        return [NONE_ENUM]

    with json_path.open("r", encoding="utf-8") as f:
        activities_data = json.load(f)

    cat = self.enum_activity_category

    if cat == "NONE" or cat not in activities_data:
        return [NONE_ENUM]

    items = [
        (key, val[0], val[1])
        for key, val in activities_data[cat].items()
    ]

    print("CATEGORY:", cat)
    print("ITEMS:", items)

    return [NONE_ENUM] + items if items else [NONE_ENUM]
def activity_category_items(self, context):
    NONE_ENUM = ("NONE", "None", "No activity category")

    toolbox = context.scene.toolBox
    json_path = Path(toolbox.string_activityfilelocation)
    if not json_path.is_file():
        return [NONE_ENUM]

    with json_path.open("r", encoding="utf-8") as f:
        activities_data = json.load(f)

    model_type = toolbox.enum_qcGen_modelType
    allowed = MODEL_TYPE_CATEGORY_MAP.get(model_type, [])

    items = [
        (cat, cat.replace("_", " "), f"Activity category: {cat}")
        for cat in activities_data.keys()
        if cat in allowed
    ]

    return [NONE_ENUM] + items if items else [NONE_ENUM]
class SequenceItem(bpy.types.PropertyGroup):
    originalName: bpy.props.StringProperty(
        name="Original Name",
        description="Original name of the sequence from the file"
    ) # type: ignore

    sequenceName: bpy.props.StringProperty(
        name="Sequence Name",
        description="User-submitted sequence name"
    ) # type: ignore

    shouldExport: bpy.props.BoolProperty(
        name="Export",
        default=True
    ) # type: ignore

    qcPath: bpy.props.StringProperty(
        name="QC Path",
        default=""
    ) # type: ignore

    customTag: bpy.props.StringProperty(
        name="Tag",
        default=""
    ) # type: ignore

    # Dynamic enums
    enum_activity_category: bpy.props.EnumProperty(
        name="Activity Category",
        items=activity_category_items,
        update=lambda self, context: setattr(self, "enum_activity", "NONE")
    ) # type: ignore

    enum_activity: bpy.props.EnumProperty(
        name="Activity",
        items=activity_item_items

    ) # type: ignore

class SequenceRigData(bpy.types.PropertyGroup):
    armatureName: bpy.props.StringProperty(
        name="Armature"
    )  # type: ignore

    sequences: bpy.props.CollectionProperty(type=SequenceItem)  # type: ignore

#----------------------------------------------------------------------
# Bodygroup PropertyGroups
#----------------------------------------------------------------------

class QC_BodygroupCollectionItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty() # type: ignore
    enabled: bpy.props.BoolProperty(
        name="Include",
        default=False
    ) # type: ignore

class QC_BodygroupBox(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(
        name="Bodygroup Name",
        default="New Bodygroup"
    ) # type: ignore
    collections: bpy.props.CollectionProperty(type=QC_BodygroupCollectionItem) # type: ignore

#----------------------------------------------------------------------
# Primary Data
#----------------------------------------------------------------------

def update_vmt_files(self, context):
    primary_data = context.scene.QC_PrimaryData
    current_count = len(primary_data.vmt_filepaths)
    target_count = primary_data.num_vmt_files

    if target_count > current_count:
        for _ in range(target_count - current_count):
            primary_data.vmt_filepaths.add()
    elif target_count < current_count:
        for _ in range(current_count - target_count):
            primary_data.vmt_filepaths.remove(len(primary_data.vmt_filepaths)-1)


class QC_PrimaryData(bpy.types.PropertyGroup):
    # Bodygroup boxes
    num_boxes: bpy.props.IntProperty(
        name="Number of Bodygroups",
        default=0,
        min=0
    ) # type: ignore
    bodygroup_boxes: bpy.props.CollectionProperty(type=QC_BodygroupBox) # type: ignore

    num_vmt_files: bpy.props.IntProperty(
        name="Number of VMTs",
        default=0,
        min=0,
        update=update_vmt_files
    ) # type: ignore
    vmt_filepaths: bpy.props.CollectionProperty(type=VMT_FilePathItem) # type: ignore

    sequence_objectdata: bpy.props.CollectionProperty(
        type=SequenceRigData
    )  # type: ignore

    attachpoint_bonenames: bpy.props.CollectionProperty(
        type=Armature_Name
    ) # type: ignore
def clearscreen():
    for i in range(5):
        print("")
def populate_filetypes_to_vtf(self, context):
    return [
        ("png", ".png", "The source file is a PNG image"),
        ("jpg", ".jpg", "The source file is a JPG/JPEG image"),
        ("jpeg", ".jpeg", "The source file is a JPEG image"),
        ("tga", ".tga", "The source file is a TGA image"),
        ("bmp", ".bmp", "The source file is a BMP image"),
        ("psd", ".psd", "The source file is a Photoshop PSD file"),
        ("hdr", ".hdr", "The source file is a HDR image"),
        ("exr", ".exr", "The source file is an OpenEXR image"),
        ("vtf", ".vtf", "The source file is already a VTF file")
    ]


#----------------------------------------------------------------------
# Toolbox / VonData Pointer
#----------------------------------------------------------------------

class VonData(bpy.types.PropertyGroup):
    float_deltaAnim_simmilarityThreshold: bpy.props.FloatProperty(
        name="Simmilarity Threshold",
        description="Percentage of bones that must match the default armature",
        default=90.0,
        min=0.0,
        max=100.0
    ) # type: ignore

     #---------------------------------------------------------------- Surface Prop
    string_surfacepropfilelocation: bpy.props.StringProperty(
        name="SurfacePropFileLoc",
        description="This is where the surfaceprop file location is....",
        default=str(Path(__file__).parent / "storeditems" / "qcgenerator" / "templates" / "surfaceprops.json"),
        subtype='FILE_PATH',
    ) # type: ignore

    def surfaceprop_category_items(self, context):
        json_path = Path(self.string_surfacepropfilelocation)
        if not json_path.is_file():
            return []
        with json_path.open("r", encoding="utf-8") as f:
            surfaceprops_data = json.load(f)
        return [(cat, cat.replace("_", " "), f"Select surfaceprop category: {cat}") 
                for cat in surfaceprops_data.keys()]

    def surfaceprop_item_items(self, context):
        json_path = Path(self.string_surfacepropfilelocation)
        if not json_path.is_file():
            return []
        with json_path.open("r", encoding="utf-8") as f:
            surfaceprops_data = json.load(f)
        cat = getattr(self, "enum_surfaceprop_category", None)
        if not cat or cat not in surfaceprops_data:
            return []
        return [(key, val[0], val[1]) for key, val in surfaceprops_data[cat].items()]


    enum_surfaceprop_category: bpy.props.EnumProperty(
        name="SurfaceProp Category",
        description="Select surfaceprop category",
        items=surfaceprop_category_items
    ) # type: ignore

    enum_surfaceprop_item: bpy.props.EnumProperty(
        name="SurfaceProp",
        description="Select surfaceprop item within category",
        items=surfaceprop_item_items
    ) # type: ignore

    #---------------------------------------------------------------- Definebones Stuff QC Gen

    string_gmodexe_path: bpy.props.StringProperty(
        name="Gmod.Exe Path",
        description="The file location of Gmod.exe for studiomdl compiler",
        default="",
        subtype='FILE_PATH',
    ) # type: ignore

    string_studiomdl_filelocation: bpy.props.StringProperty(
        name="Studiomdl File Location",
        description="This is where the surfaceprop file location is....",
        default=str(Path(__file__).parent / "storeditems" / "external_software_dependancies" / "studiomdl" / "bin" / "studiomdl.exe"),
        subtype='FILE_PATH',
    ) # type: ignore

    bool_studiomdl_verbose : bpy.props.BoolProperty(
        name = "Print Results?",
        description = "",
        default = False
    ) # type: ignore


     #---------------------------------------------------------------- QC Generator Stuff (SIMPLE)


    enum_qcGen_charAnimIncludes : bpy.props.EnumProperty(
        name="Include Char Anims?",
        description="For character and NPC models, do you want to include base animations, and if so what type?",
        items = [("None","None","Do not include existing animations. Best for use if you are not using the default valve.biped armature"),("f_anm.mdl", "Female", "Include the base female animations"), ("m_anm.mdl", "Male", "Include the base male animations"),("z_anm.mdl","Zombie","Include the base zombie animations")],
        default = "None"
    ) # type: ignore

    enum_qcGen_modelType : bpy.props.EnumProperty(
        name="QC Type",
        description="Type of model you're making a QC for, is it a prop, character, npc?",
        items =  [
            ('PROP', "Prop", "Standard physics prop"),
            ('CHARACTER', "Character", "Player or character model"),
            ('NPC', "Npc", "Non-player character model"),
            ('VIEWMODEL', "Viewmodel", "First-person view model"),
            ('WORLDMODEL', "Worldmodel", "Third-person world model"),
        ],
        default = "CHARACTER"
    ) # type: ignore
    
    #-----------------------------------------------------


    #-----------------------------------------------------

    string_activityfilelocation: bpy.props.StringProperty(
        name="Activity JSON File",
        default=str(Path(__file__).parent / "storeditems" / "qcgenerator" / "templates" / "activities.json"),
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

    # Smd Batch Exporter

    string_export_folder: bpy.props.StringProperty(
        name="Export Folder",
        description="Folder to save exported SMDs",
        default="//",
        subtype='DIR_PATH'
    ) # type: ignore

#---------------------------------------------------------------- QC Generator ADVANCED (SIMPLE)


    int_qcGen_scale : bpy.props.IntProperty(
        name = "Character Scale",
        description = "Scale of the characeter",
        default = 1,
        soft_min = 0,
        soft_max = 10,
        step = 1
    ) # type: ignore

    bool_qcGen_incDefaultCharAnim : bpy.props.BoolProperty(
        name = "Include Default Char Animations?",
        description = "Should include anm_m, ect?",
        default = False
    ) # type: ignore

    bool_qcGen_shouldDefineBones : bpy.props.BoolProperty(
        name = "Generate Definebones.qci?",
        description = "Should a definebones.qci be generated?",
        default = False
    ) # type: ignore

#---------------------------------------------------------------- vtf batch conversions

    
    
    string_vtfbatch_vtfccmdexe: bpy.props.StringProperty(
        name="VTFCmd Executable",
        description="Path to VTFCmd.exe",
        default=str(Path(__file__).parent / "storeditems" / "external_software_dependancies" / "vtfcmd" / "VTFCmd.exe"),
        subtype='FILE_PATH'
    )  # type: ignore

    string_vtfbatch_inputfolder: bpy.props.StringProperty(
        name="Input Folder",
        description="Folder containing files to convert",
        default="",
        subtype='DIR_PATH'
    )  # type: ignore

    string_vtfbatch_outputfolder: bpy.props.StringProperty(
        name="Output Folder",
        description="Folder to save converted files",
        default="",
        subtype='DIR_PATH'
    )  # type: ignore

    enum_vtfbatch_sourcefiletype: bpy.props.EnumProperty(
        name="Source Filetype",
        description="Choose the source file type for conversion",
        items=populate_filetypes_to_vtf,
        default=0
    ) # type: ignore

    # Target filetype enum (dynamic, excludes source)
    def populate_target_filetypes(self, context):
        source = context.scene.toolBox.enum_vtfbatch_sourcefiletype
        return [item for item in populate_filetypes_to_vtf(self, context) if item[0] != source]

    enum_vtfbatch_targetfiletype: bpy.props.EnumProperty(
        name="Target Filetype",
        description="Choose the target file type for conversion",
        items=populate_target_filetypes,
        default=0
    ) # type: ignore



#----------------------------------------------------------------------
# Bodygroup Sync Helper
#----------------------------------------------------------------------

def sync_bodygroup_boxes(scene):
    """Ensure the bodygroup_boxes collection matches num_boxes."""
    qcData = scene.QC_PrimaryData
    existing_collections = [col.name for col in bpy.data.collections]

    while len(qcData.bodygroup_boxes) < qcData.num_boxes:
        qcData.bodygroup_boxes.add()

    while len(qcData.bodygroup_boxes) > qcData.num_boxes:
        qcData.bodygroup_boxes.remove(len(qcData.bodygroup_boxes)-1)

    for box in qcData.bodygroup_boxes:
        existing_names = {item.name for item in box.collections}
        for name in existing_collections:
            if name not in existing_names:
                item = box.collections.add()
                item.name = name
                item.enabled = False

def get_bodygroup_by_name(qcData, box_name):
    for box in qcData.bodygroup_boxes:
        if box.name == box_name:
            return box
    return None

def get_sequences_dict(primaryData):
    sequencesDict = {}
    primaryData = bpy.context.scene.QC_PrimaryData
    for rigData in primaryData.sequence_objectdata:
        rigName = rigData.armatureName
        sequenceNames = [seq.sequenceName for seq in rigData.sequences]
        sequencesDict[rigName] = sequenceNames
    return sequencesDict # { RigName: [SequenceName, ect], RigName2, ectectect }

#----------------------------------------------------------------------
# Registration
#----------------------------------------------------------------------

classes = [
    #attachment points
    Bone_NameForAttach,
    Armature_Name,
    
    # Bodygroup
    QC_BodygroupCollectionItem,
    QC_BodygroupBox,

    #Sequence
    SequenceItem,
    SequenceRigData,

    # VMT
    VMT_FilePathItem,

    # Primary Data
    QC_PrimaryData,

    # Toolbox
    VonData,
]

def von_common_register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Pointer properties on the scene
    bpy.types.Scene.QC_PrimaryData = bpy.props.PointerProperty(type=QC_PrimaryData)
    bpy.types.Scene.toolBox = bpy.props.PointerProperty(type=VonData)

def von_common_unregister():
    del bpy.types.Scene.QC_PrimaryData
    del bpy.types.Scene.toolBox

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)