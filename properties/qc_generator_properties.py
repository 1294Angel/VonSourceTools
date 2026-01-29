"""
Properties for QC Generator panel.

This module contains all properties displayed in the QC Generator panel
and its sub-panels (Bodygroups, Materials, Animations, Advanced).
"""
import json
import bpy  # type: ignore
from bpy.props import (
    StringProperty, BoolProperty, IntProperty,
    EnumProperty, CollectionProperty
)
from pathlib import Path


# ============================================================================
# Surface Property Helpers
# ============================================================================

def _get_bundled_surfaceprops_path():
    """Get the bundled surfaceprops.json path."""
    this_file = Path(__file__).resolve()
    addon_root = this_file.parent.parent  # properties -> refactor
    return addon_root / "storeditems" / "qcgenerator" / "templates" / "surfaceprops.json"


def _load_surfaceprops_data(custom_path=""):
    """Load surface properties data from JSON file."""
    # Try custom path first
    if custom_path:
        custom = Path(custom_path)
        if custom.is_file():
            try:
                with custom.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    
    # Fall back to bundled
    bundled = _get_bundled_surfaceprops_path()
    if bundled.is_file():
        try:
            with bundled.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    
    return None


def surfaceprop_category_items_callback(self, context):
    """Get surface property categories from JSON file."""
    custom_path = getattr(self, "string_surfacepropfilelocation", "")
    data = _load_surfaceprops_data(custom_path)
    
    if not data:
        return [("NONE", "None", "No surface properties file found")]
    
    items = [
        (cat, cat.replace("_", " "), f"Select surfaceprop category: {cat}")
        for cat in data.keys()
    ]
    return items if items else [("NONE", "None", "No categories found")]


def surfaceprop_item_items_callback(self, context):
    """Get surface property items for the selected category."""
    custom_path = getattr(self, "string_surfacepropfilelocation", "")
    data = _load_surfaceprops_data(custom_path)
    
    if not data:
        return [("NONE", "None", "No surface properties file found")]
    
    cat = getattr(self, "enum_surfaceprop_category", None)
    if not cat or cat == "NONE" or cat not in data:
        return [("NONE", "None", "Select a category first")]
    
    items = [
        (key, val[0], val[1])
        for key, val in data[cat].items()
    ]
    return items if items else [("NONE", "None", "No items in category")]


# ============================================================================
# Bodygroup/VMT Helper Functions
# ============================================================================

def update_vmt_files(self, context):
    """Sync VMT file collection with num_vmt_files count."""
    primary_data = context.scene.von_qc_data
    current_count = len(primary_data.vmt_filepaths)
    target_count = primary_data.num_vmt_files
    
    if target_count > current_count:
        for _ in range(target_count - current_count):
            primary_data.vmt_filepaths.add()
    elif target_count < current_count:
        for _ in range(current_count - target_count):
            primary_data.vmt_filepaths.remove(len(primary_data.vmt_filepaths) - 1)


def sync_bodygroup_boxes(scene):
    """Ensure the bodygroup_boxes collection matches num_boxes."""
    qc_data = scene.von_qc_data
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
# Sub-Property Groups (for collections)
# ============================================================================

class VMT_FilePathItem(bpy.types.PropertyGroup):
    """Single VMT file path entry for cdmaterials."""
    filepath: StringProperty(
        name="File Path",
        description="Path to VMT file or material folder",
        subtype='FILE_PATH'
    )  # type: ignore


class BodygroupCollectionItem(bpy.types.PropertyGroup):
    """A collection that can be included in a bodygroup."""
    name: StringProperty(
        name="Collection Name"
    )  # type: ignore
    enabled: BoolProperty(
        name="Include",
        description="Include this collection in the bodygroup",
        default=False
    )  # type: ignore


class BodygroupBox(bpy.types.PropertyGroup):
    """A bodygroup containing multiple collection options."""
    name: StringProperty(
        name="Bodygroup Name",
        description="Name of this bodygroup in the QC file",
        default="New Bodygroup"
    )  # type: ignore
    collections: CollectionProperty(
        type=BodygroupCollectionItem,
        name="Collections"
    )  # type: ignore


class BoneNameForAttach(bpy.types.PropertyGroup):
    """Bone name for attachment point."""
    bonename: StringProperty(
        name="Bone Name"
    )  # type: ignore


class ArmatureName(bpy.types.PropertyGroup):
    """Armature reference with attachment sequences."""
    armatureName: StringProperty(
        name="Armature"
    )  # type: ignore
    sequences: CollectionProperty(
        type=BoneNameForAttach
    )  # type: ignore


# ============================================================================
# QC Primary Data Property Group
# ============================================================================

class QC_PrimaryData(bpy.types.PropertyGroup):
    """
    Main QC generation data container.
    
    Stores collections of bodygroups, material paths, sequences, and attachments
    that are used to generate QC files.
    """
    # Import SequenceRigData at runtime to avoid circular imports
    
    # Bodygroup settings
    num_boxes: IntProperty(
        name="Number of Bodygroups",
        default=0,
        min=0
    )  # type: ignore
    
    bodygroup_boxes: CollectionProperty(
        type=BodygroupBox
    )  # type: ignore
    
    # VMT/Material path settings
    num_vmt_files: IntProperty(
        name="Number of VMTs",
        default=0,
        min=0,
        update=update_vmt_files
    )  # type: ignore
    
    vmt_filepaths: CollectionProperty(
        type=VMT_FilePathItem
    )  # type: ignore
    
    # Attachment points
    attachpoint_bonenames: CollectionProperty(
        type=ArmatureName
    )  # type: ignore


# Add sequence_objectdata after SequenceRigData is registered
def _add_sequence_collection():
    """Add sequence collection to QC_PrimaryData after SequenceRigData is registered."""
    from .sequence_properties import SequenceRigData
    
    if not hasattr(QC_PrimaryData, 'sequence_objectdata'):
        QC_PrimaryData.sequence_objectdata = CollectionProperty(
            type=SequenceRigData
        )


# ============================================================================
# QC Generator Settings Property Group
# ============================================================================

def _get_default_studiomdl_path():
    """Get default studiomdl path for property default."""
    from ..data.paths import get_default_studiomdl_path
    return get_default_studiomdl_path()


class QCGeneratorSettings(bpy.types.PropertyGroup):
    """
    Settings for the QC Generator panel.
    
    Contains model type, output paths, surface properties, collision settings,
    and StudioMDL configuration.
    """
    
    # ----- Model Settings -----
    enum_modelType: EnumProperty(
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
    
    string_mdlModelName: StringProperty(
        name="Model Name",
        description="Final name of the compiled asset",
        default="",
    )  # type: ignore
    
    string_outputPath: StringProperty(
        name="Output Filepath",
        description="Filepath the created QC file will output to",
        default="",
        subtype='DIR_PATH'
    )  # type: ignore
    
    string_materialPath: StringProperty(
        name="Material Subfolder Filepath",
        description="Filepath after the materials folder where VMT files are located",
        default="",
        subtype='DIR_PATH'
    )  # type: ignore
    
    int_scale: IntProperty(
        name="Character Scale",
        description="Scale of the character",
        default=1,
        soft_min=0,
        soft_max=10,
        step=1
    )  # type: ignore
    
    # ----- Collision Settings -----
    bool_generateCollision: BoolProperty(
        name="Generate Collisions?",
        description="Should collisions be automatically generated?",
        default=False
    )  # type: ignore
    
    string_existingCollisionCollection: StringProperty(
        name="Existing Collision Collection",
        description="Name of the existing collision mesh collection",
        default="",
    )  # type: ignore
    
    # ----- Surface Property Settings -----
    string_surfacepropFileLocation: StringProperty(
        name="SurfaceProp File Location",
        description="Path to the surfaceprops.json file (leave empty to use bundled)",
        default="",
        subtype='FILE_PATH',
    )  # type: ignore
    
    enum_surfaceprop_category: EnumProperty(
        name="SurfaceProp Category",
        description="Select surfaceprop category",
        items=surfaceprop_category_items_callback
    )  # type: ignore
    
    enum_surfaceprop_item: EnumProperty(
        name="SurfaceProp",
        description="Select surfaceprop item within category",
        items=surfaceprop_item_items_callback
    )  # type: ignore
    
    # ----- Animation Settings -----
    string_activityFileLocation: StringProperty(
        name="Activity JSON File",
        default="",
    )  # type: ignore
    
    enum_charAnimIncludes: EnumProperty(
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
    
    bool_incDefaultCharAnim: BoolProperty(
        name="Include Default Char Animations?",
        description="Should include anm_m, etc?",
        default=False
    )  # type: ignore
    
    # ----- DefineBones Settings -----
    bool_shouldDefineBones: BoolProperty(
        name="Generate Definebones.qci?",
        description="Should a definebones.qci be generated?",
        default=False
    )  # type: ignore
    
    # ----- StudioMDL Settings -----
    string_studiomdlFileLocation: StringProperty(
        name="StudioMDL File Location",
        description="Path to studiomdl.exe",
        default="",
        subtype='FILE_PATH',
    )  # type: ignore
    
    string_gmodExePath: StringProperty(
        name="Gmod.Exe Path",
        description="The file location of Gmod.exe for studiomdl compiler",
        default="",
        subtype='FILE_PATH',
    )  # type: ignore
    
    bool_studiomdlVerbose: BoolProperty(
        name="Print Results?",
        description="Print studiomdl output to console",
        default=False
    )  # type: ignore


# ============================================================================
# Registration
# ============================================================================

CLASSES = [
    VMT_FilePathItem,
    BodygroupCollectionItem,
    BodygroupBox,
    BoneNameForAttach,
    ArmatureName,
    QC_PrimaryData,
    QCGeneratorSettings,
]


def register():
    """Register all QC Generator property groups."""
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    
    # Add sequence collection after SequenceRigData is registered
    _add_sequence_collection()


def unregister():
    """Unregister all QC Generator property groups."""
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
