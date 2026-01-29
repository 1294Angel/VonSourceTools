"""
Properties for Delta Animation Trick panel.

This module contains all properties displayed in the Delta Animation Trick panel.
"""
import bpy  # type: ignore
from bpy.props import FloatProperty


# ============================================================================
# Delta Animation Settings Property Group
# ============================================================================

class DeltaAnimSettings(bpy.types.PropertyGroup):
    """
    Settings for the Delta Animation Trick panel.
    
    Used to configure how delta animations are generated from armatures.
    """
    
    float_similarityThreshold: FloatProperty(
        name="Similarity Threshold",
        description="Percentage of bones that must match the default armature",
        default=90.0,
        min=0.0,
        max=100.0
    )  # type: ignore


# ============================================================================
# Registration
# ============================================================================

CLASSES = [
    DeltaAnimSettings,
]


def register():
    """Register all Delta Animation property groups."""
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister all Delta Animation property groups."""
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
