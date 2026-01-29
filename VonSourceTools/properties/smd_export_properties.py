"""
Properties for Batch SMD Export panel.

This module contains all properties displayed in the Batch SMD Export panel.
"""
import bpy  # type: ignore
from bpy.props import StringProperty


# ============================================================================
# SMD Export Settings Property Group
# ============================================================================

class SMDExportSettings(bpy.types.PropertyGroup):
    """
    Settings for the Batch SMD Export panel.
    
    Used to configure batch SMD file exporting from collections.
    """
    
    string_exportFolder: StringProperty(
        name="Export Folder",
        description="Folder to save exported SMD files",
        default="//",
        subtype='DIR_PATH'
    )  # type: ignore


# ============================================================================
# Registration
# ============================================================================

CLASSES = [
    SMDExportSettings,
]


def register():
    """Register all SMD Export property groups."""
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister all SMD Export property groups."""
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
