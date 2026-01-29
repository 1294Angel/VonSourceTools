"""
Properties for Image Filetype Converter panel.

This module contains all properties displayed in the Image Filetype Converter panel.
Used for batch converting between image formats (PNG, JPG, TGA, VTF, etc.).
"""
import bpy  # type: ignore
from bpy.props import StringProperty, EnumProperty


# ============================================================================
# Helper Functions
# ============================================================================

def _get_default_vtfcmd_path():
    """Get default VTFCmd path for property default."""
    from ..data.paths import get_default_vtfcmd_path
    return get_default_vtfcmd_path()


def populate_filetypes(self, context):
    """Get supported file types for conversion."""
    return [
        ("png", ".png", "PNG image format"),
        ("jpg", ".jpg", "JPG/JPEG image format"),
        ("jpeg", ".jpeg", "JPEG image format"),
        ("tga", ".tga", "TGA image format"),
        ("bmp", ".bmp", "BMP image format"),
        ("psd", ".psd", "Photoshop PSD file"),
        ("hdr", ".hdr", "HDR image format"),
        ("exr", ".exr", "OpenEXR image format"),
        ("vtf", ".vtf", "Valve Texture Format (VTF)")
    ]


def populate_target_filetypes(self, context):
    """Get target file types, excluding currently selected source type."""
    source = self.enum_sourceFiletype
    return [
        item for item in populate_filetypes(self, context)
        if item[0] != source
    ]


# ============================================================================
# Image Converter Settings Property Group
# ============================================================================

class ImageConverterSettings(bpy.types.PropertyGroup):
    """
    Settings for the Image Filetype Converter panel.
    
    Used to configure batch image format conversion.
    """
    
    string_vtfcmdPath: StringProperty(
        name="VTFCmd Executable",
        description="Path to VTFCmd.exe (for VTF conversions)",
        default="",
        subtype='FILE_PATH'
    )  # type: ignore
    
    string_inputFolder: StringProperty(
        name="Input Folder",
        description="Folder containing files to convert",
        default="",
        subtype='DIR_PATH'
    )  # type: ignore
    
    string_outputFolder: StringProperty(
        name="Output Folder",
        description="Folder to save converted files",
        default="",
        subtype='DIR_PATH'
    )  # type: ignore
    
    enum_sourceFiletype: EnumProperty(
        name="Source Filetype",
        description="Choose the source file type for conversion",
        items=populate_filetypes,
        default=0
    )  # type: ignore
    
    enum_targetFiletype: EnumProperty(
        name="Target Filetype",
        description="Choose the target file type for conversion",
        items=populate_target_filetypes,
        default=0
    )  # type: ignore


# ============================================================================
# Registration
# ============================================================================

CLASSES = [
    ImageConverterSettings,
]


def register():
    """Register all Image Converter property groups."""
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister all Image Converter property groups."""
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
