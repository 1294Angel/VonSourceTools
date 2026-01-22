import bpy,json# type: ignore
from pathlib import Path
##----------------------------------------------------------------------
# Harded Coded File Locs
#----------------------------------------------------------------------
default_surfaceprop_path = str(Path(__file__).parent / "storeditems" / "qcgenerator" / "templates" / "surfaceprops.json")


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
#----------------------------------------------------------------------
# QC Data Updates
#----------------------------------------------------------------------

def qc_file_types():
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

#----------------------------------------------------------------------
# VMT Filepath Storage
#----------------------------------------------------------------------

class VMT_FilePathItem(bpy.types.PropertyGroup):
    filepath: bpy.props.StringProperty(
        name="File Path",
        subtype='FILE_PATH'
    ) # type: ignore

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
    """Automatically sync vmt_filepaths collection to num_vmt_files."""
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

    export_folder: bpy.props.StringProperty(
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



#----------------------------------------------------------------------
# Registration
#----------------------------------------------------------------------

classes = [
    # Bodygroup
    QC_BodygroupCollectionItem,
    QC_BodygroupBox,

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