"""
Main toolbox property groups for VonSourceTools.
"""
import json
import bpy  # type: ignore
from bpy.props import (
    StringProperty, BoolProperty, IntProperty, FloatProperty,
    EnumProperty, CollectionProperty, PointerProperty
)
from pathlib import Path

from .qc_properties import (
    VMT_FilePathItem, BodygroupBox, ArmatureName
)
from .sequence_properties import SequenceRigData


# ============================================================================
# Helper Functions
# ============================================================================

def update_vmt_files(self, context):
    """Sync VMT file collection with num_vmt_files count."""
    primary_data = context.scene.QC_PrimaryData
    current_count = len(primary_data.vmt_filepaths)
    target_count = primary_data.num_vmt_files
    
    if target_count > current_count:
        for _ in range(target_count - current_count):
            primary_data.vmt_filepaths.add()
    elif target_count < current_count:
        for _ in range(current_count - target_count):
            primary_data.vmt_filepaths.remove(len(primary_data.vmt_filepaths) - 1)


def populate_filetypes_to_vtf(self, context):
    """Get supported file types for VTF conversion."""
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


def sync_bodygroup_boxes(scene):
    """Ensure the bodygroup_boxes collection matches num_boxes."""
    qc_data = scene.QC_PrimaryData
    existing_collections = [col.name for col in bpy.data.collections]
    
    while len(qc_data.bodygroup_boxes) < qc_data.num_boxes:
        qc_data.bodygroup_boxes.add()
    
    while len(qc_data.bodygroup_boxes) > qc_data.num_boxes:
        qc_data.bodygroup_boxes.remove(len(qc_data.bodygroup_boxes) - 1)
    
    for box in qc_data.bodygroup_boxes:
        existing_names = {item.name for item in box.collections}
        for name in existing_collections:
            if name not in existing_names:
                item = box.collections.add()
                item.name = name
                item.enabled = False


def get_bodygroup_by_name(qc_data, box_name):
    """Find a bodygroup by name."""
    for box in qc_data.bodygroup_boxes:
        if box.name == box_name:
            return box
    return None


# ============================================================================
# Primary Data Property Group
# ============================================================================

class QC_PrimaryData(bpy.types.PropertyGroup):
    """Main QC generation data container."""
    
    # Bodygroup settings
    num_boxes: IntProperty(
        name="Number of Bodygroups",
        default=0,
        min=0
    )  # type: ignore
    
    bodygroup_boxes: CollectionProperty(
        type=BodygroupBox
    )  # type: ignore
    
    # VMT settings
    num_vmt_files: IntProperty(
        name="Number of VMTs",
        default=0,
        min=0,
        update=update_vmt_files
    )  # type: ignore
    
    vmt_filepaths: CollectionProperty(
        type=VMT_FilePathItem
    )  # type: ignore
    
    # Sequence data
    sequence_objectdata: CollectionProperty(
        type=SequenceRigData
    )  # type: ignore
    
    # Attachment points
    attachpoint_bonenames: CollectionProperty(
        type=ArmatureName
    )  # type: ignore


# ============================================================================
# Main Toolbox Property Group
# ============================================================================

class VonToolbox(bpy.types.PropertyGroup):
    """Main toolbox settings for VonSourceTools."""
    
    # -------------------------------------------------------------------------
    # Delta Animation Settings
    # -------------------------------------------------------------------------
    float_deltaAnim_similarityThreshold: FloatProperty(
        name="Similarity Threshold",
        description="Percentage of bones that must match the default armature",
        default=90.0,
        min=0.0,
        max=100.0
    )  # type: ignore
    
    # -------------------------------------------------------------------------
    # Surface Prop Settings
    # -------------------------------------------------------------------------
    string_surfacepropfilelocation: StringProperty(
        name="SurfaceProp File Location",
        description="Path to the surfaceprops.json file",
        default="",
        subtype='FILE_PATH',
    )  # type: ignore
    
    def surfaceprop_category_items(self, context):
        json_path = Path(self.string_surfacepropfilelocation)
        if not json_path.is_file():
            return []
        with json_path.open("r", encoding="utf-8") as f:
            surfaceprops_data = json.load(f)
        return [
            (cat, cat.replace("_", " "), f"Select surfaceprop category: {cat}")
            for cat in surfaceprops_data.keys()
        ]
    
    def surfaceprop_item_items(self, context):
        json_path = Path(self.string_surfacepropfilelocation)
        if not json_path.is_file():
            return []
        with json_path.open("r", encoding="utf-8") as f:
            surfaceprops_data = json.load(f)
        cat = getattr(self, "enum_surfaceprop_category", None)
        if not cat or cat not in surfaceprops_data:
            return []
        return [
            (key, val[0], val[1])
            for key, val in surfaceprops_data[cat].items()
        ]
    
    enum_surfaceprop_category: EnumProperty(
        name="SurfaceProp Category",
        description="Select surfaceprop category",
        items=surfaceprop_category_items
    )  # type: ignore
    
    enum_surfaceprop_item: EnumProperty(
        name="SurfaceProp",
        description="Select surfaceprop item within category",
        items=surfaceprop_item_items
    )  # type: ignore
    
    # -------------------------------------------------------------------------
    # StudioMDL / DefineBones Settings
    # -------------------------------------------------------------------------
    string_gmodexe_path: StringProperty(
        name="Gmod.Exe Path",
        description="The file location of Gmod.exe for studiomdl compiler",
        default="",
        subtype='FILE_PATH',
    )  # type: ignore
    
    string_studiomdl_filelocation: StringProperty(
        name="StudioMDL File Location",
        description="Path to studiomdl.exe",
        default="",
        subtype='FILE_PATH',
    )  # type: ignore
    
    bool_studiomdl_verbose: BoolProperty(
        name="Print Results?",
        description="Print studiomdl output to console",
        default=False
    )  # type: ignore
    
    # -------------------------------------------------------------------------
    # QC Generator Settings
    # -------------------------------------------------------------------------
    string_activityfilelocation: StringProperty(
        name="Activity JSON File",
        default="",
    )  # type: ignore
    
    enum_qcGen_charAnimIncludes: EnumProperty(
        name="Include Char Anims?",
        description="For character and NPC models, include base animations?",
        items=[
            ("None", "None", "Do not include existing animations"),
            ("f_anm.mdl", "Female", "Include the base female animations"),
            ("m_anm.mdl", "Male", "Include the base male animations"),
            ("z_anm.mdl", "Zombie", "Include the base zombie animations")
        ],
        default="None"
    )  # type: ignore
    
    enum_qcGen_modelType: EnumProperty(
        name="QC Type",
        description="Type of model you're making a QC for",
        items=[
            ('PROP', "Prop", "Standard physics prop"),
            ('CHARACTER', "Character", "Player or character model"),
            ('NPC', "NPC", "Non-player character model"),
            ('VIEWMODEL', "Viewmodel", "First-person view model"),
            ('WORLDMODEL', "Worldmodel", "Third-person world model"),
        ],
        default="CHARACTER"
    )  # type: ignore
    
    string_qcGen_outputPath: StringProperty(
        name="Output Filepath",
        description="Filepath the created QC file will output to",
        default="",
        subtype='FILE_PATH'
    )  # type: ignore
    
    string_qcGen_materialPath: StringProperty(
        name="Material Subfolder Filepath",
        description="Filepath after the materials folder where VMT files are located",
        default="",
        subtype='FILE_PATH'
    )  # type: ignore
    
    bool_qcGen_generateCollission: BoolProperty(
        name="Generate Collisions?",
        description="Should collisions be automatically generated?",
        default=False
    )  # type: ignore
    
    string_qcGen_existingCollissionCollection: StringProperty(
        name="Existing Collision Collection",
        description="Name of the existing collision mesh collection",
        default="",
    )  # type: ignore
    
    string_qcGen_mdlModelName: StringProperty(
        name="Model Name",
        description="Final name of the compiled asset",
        default="",
    )  # type: ignore
    
    int_qcGen_scale: IntProperty(
        name="Character Scale",
        description="Scale of the character",
        default=1,
        soft_min=0,
        soft_max=10,
        step=1
    )  # type: ignore
    
    bool_qcGen_incDefaultCharAnim: BoolProperty(
        name="Include Default Char Animations?",
        description="Should include anm_m, etc?",
        default=False
    )  # type: ignore
    
    bool_qcGen_shouldDefineBones: BoolProperty(
        name="Generate Definebones.qci?",
        description="Should a definebones.qci be generated?",
        default=False
    )  # type: ignore
    
    # -------------------------------------------------------------------------
    # SMD Export Settings
    # -------------------------------------------------------------------------
    string_export_folder: StringProperty(
        name="Export Folder",
        description="Folder to save exported SMDs",
        default="//",
        subtype='DIR_PATH'
    )  # type: ignore
    
    # -------------------------------------------------------------------------
    # VTF Batch Conversion Settings
    # -------------------------------------------------------------------------
    string_vtfbatch_vtfccmdexe: StringProperty(
        name="VTFCmd Executable",
        description="Path to VTFCmd.exe",
        default="",
        subtype='FILE_PATH'
    )  # type: ignore
    
    string_vtfbatch_inputfolder: StringProperty(
        name="Input Folder",
        description="Folder containing files to convert",
        default="",
        subtype='DIR_PATH'
    )  # type: ignore
    
    string_vtfbatch_outputfolder: StringProperty(
        name="Output Folder",
        description="Folder to save converted files",
        default="",
        subtype='DIR_PATH'
    )  # type: ignore
    
    enum_vtfbatch_sourcefiletype: EnumProperty(
        name="Source Filetype",
        description="Choose the source file type for conversion",
        items=populate_filetypes_to_vtf,
        default=0
    )  # type: ignore
    
    def populate_target_filetypes(self, context):
        source = context.scene.toolBox.enum_vtfbatch_sourcefiletype
        return [
            item for item in populate_filetypes_to_vtf(self, context)
            if item[0] != source
        ]
    
    enum_vtfbatch_targetfiletype: EnumProperty(
        name="Target Filetype",
        description="Choose the target file type for conversion",
        items=populate_target_filetypes,
        default=0
    )  # type: ignore


# ============================================================================
# Registration
# ============================================================================

CLASSES = [
    QC_PrimaryData,
    VonToolbox,
]


def register():
    """Register all property groups in this module."""
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    
    # Attach to scene
    bpy.types.Scene.QC_PrimaryData = PointerProperty(type=QC_PrimaryData)
    bpy.types.Scene.toolBox = PointerProperty(type=VonToolbox)


def unregister():
    """Unregister all property groups in this module."""
    del bpy.types.Scene.QC_PrimaryData
    del bpy.types.Scene.toolBox
    
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
