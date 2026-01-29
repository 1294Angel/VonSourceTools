"""
Legacy toolbox properties for backwards compatibility.

This module provides the old VonToolbox and QC_PrimaryData classes
that wrap the new organized property system. This ensures existing
code and UI panels continue to work while we transition to the new system.

NEW CODE SHOULD USE:
- von_qc_settings for QC Generator settings
- von_qc_data for QC primary data
- von_delta_anim for Delta Animation settings
- von_image_converter for Image Converter settings
- von_smd_export for SMD Export settings
"""
import bpy  # type: ignore
from bpy.props import (
    StringProperty, BoolProperty, IntProperty, FloatProperty,
    EnumProperty, CollectionProperty, PointerProperty
)

# Import from new modules for re-export
from .qc_generator_properties import (
    QC_PrimaryData,
    VMT_FilePathItem,
    BodygroupBox,
    BodygroupCollectionItem,
    ArmatureName,
    BoneNameForAttach,
    sync_bodygroup_boxes,
    get_bodygroup_by_name,
    update_vmt_files,
    surfaceprop_category_items_callback,
    surfaceprop_item_items_callback,
)
from .image_converter_properties import populate_filetypes


# ============================================================================
# Legacy VonToolbox Property Group
# ============================================================================

class VonToolbox(bpy.types.PropertyGroup):
    """
    Legacy main toolbox settings for VonSourceTools.
    
    This class maintains backwards compatibility with existing UI panels
    and operators. New code should access properties through the new
    organized scene properties (von_qc_settings, von_delta_anim, etc.).
    """
    
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
    # Surface Prop Settings (QC Generator)
    # -------------------------------------------------------------------------
    string_surfacepropfilelocation: StringProperty(
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
    
    # -------------------------------------------------------------------------
    # StudioMDL / DefineBones Settings (QC Generator)
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
    # VTF Batch Conversion Settings (Image Converter)
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
        items=populate_filetypes,
        default=0
    )  # type: ignore
    
    def populate_target_filetypes(self, context):
        source = context.scene.toolBox.enum_vtfbatch_sourcefiletype
        return [
            item for item in populate_filetypes(self, context)
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
    VonToolbox,
]


def register():
    """Register legacy property groups."""
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    
    # Attach legacy properties to scene
    bpy.types.Scene.QC_PrimaryData = PointerProperty(type=QC_PrimaryData)
    bpy.types.Scene.toolBox = PointerProperty(type=VonToolbox)


def unregister():
    """Unregister legacy property groups."""
    # Remove scene properties
    if hasattr(bpy.types.Scene, 'QC_PrimaryData'):
        del bpy.types.Scene.QC_PrimaryData
    if hasattr(bpy.types.Scene, 'toolBox'):
        del bpy.types.Scene.toolBox
    
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
