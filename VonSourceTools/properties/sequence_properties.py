"""
Properties for animation sequence data.

Used by the QC Generator for managing animation sequences.
"""
import json
import bpy  # type: ignore
from bpy.props import (
    StringProperty, BoolProperty, EnumProperty,
    CollectionProperty
)
from pathlib import Path

from ..data.constants import MODEL_TYPE_CATEGORY_MAP, NONE_ENUM


# ============================================================================
# Helper Functions
# ============================================================================

def _get_bundled_activities_path():
    """Get the bundled activities.json path."""
    this_file = Path(__file__).resolve()
    addon_root = this_file.parent.parent  # properties -> refactor
    return addon_root / "storeditems" / "qcgenerator" / "templates" / "activities.json"


def _load_activities_data(custom_path=""):
    """Load activities data from JSON file."""
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
    bundled = _get_bundled_activities_path()
    if bundled.is_file():
        try:
            with bundled.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    
    return None


def _get_model_type(context):
    """Get the current model type from scene settings."""
    # Try new property names first, then fall back to legacy
    if hasattr(context.scene, 'von_qc_settings'):
        return getattr(context.scene.von_qc_settings, 'enum_modelType', 'CHARACTER')
    elif hasattr(context.scene, 'toolBox'):
        return getattr(context.scene.toolBox, 'enum_qcGen_modelType', 'CHARACTER')
    return 'CHARACTER'


def _get_activity_file_path(context):
    """Get the activity file path from scene settings."""
    # Try new property names first, then fall back to legacy
    if hasattr(context.scene, 'von_qc_settings'):
        return getattr(context.scene.von_qc_settings, 'string_activityFileLocation', '')
    elif hasattr(context.scene, 'toolBox'):
        return getattr(context.scene.toolBox, 'string_activityfilelocation', '')
    return ''


def activity_item_items(self, context):
    """Generate activity items based on selected category."""
    none_enum = ("NONE", "None", "Do not replace any activity")
    
    custom_path = _get_activity_file_path(context)
    activities_data = _load_activities_data(custom_path)
    
    if not activities_data:
        return [none_enum]
    
    cat = self.enum_activity_category
    
    if cat == "NONE" or cat not in activities_data:
        return [none_enum]
    
    items = [
        (key, val[0], val[1])
        for key, val in activities_data[cat].items()
    ]
    
    return [none_enum] + items if items else [none_enum]


def activity_category_items(self, context):
    """Generate activity category items based on model type."""
    none_enum = ("NONE", "None", "No activity category")
    
    custom_path = _get_activity_file_path(context)
    activities_data = _load_activities_data(custom_path)
    
    if not activities_data:
        return [none_enum]
    
    model_type = _get_model_type(context)
    allowed = MODEL_TYPE_CATEGORY_MAP.get(model_type, [])
    
    items = [
        (cat, cat.replace("_", " "), f"Activity category: {cat}")
        for cat in activities_data.keys()
        if cat in allowed
    ]
    
    return [none_enum] + items if items else [none_enum]


# ============================================================================
# Property Groups
# ============================================================================

class SequenceItem(bpy.types.PropertyGroup):
    """Single animation sequence with metadata."""
    originalName: StringProperty(
        name="Original Name",
        description="Original name of the sequence from the file"
    )  # type: ignore
    
    sequenceName: StringProperty(
        name="Sequence Name",
        description="User-submitted sequence name"
    )  # type: ignore
    
    shouldExport: BoolProperty(
        name="Export",
        default=True
    )  # type: ignore
    
    qcPath: StringProperty(
        name="QC Path",
        default=""
    )  # type: ignore
    
    customTag: StringProperty(
        name="Tag",
        default=""
    )  # type: ignore
    
    enum_activity_category: EnumProperty(
        name="Activity Category",
        items=activity_category_items,
        update=lambda self, context: setattr(self, "enum_activity", "NONE")
    )  # type: ignore
    
    enum_activity: EnumProperty(
        name="Activity",
        items=activity_item_items
    )  # type: ignore


class SequenceRigData(bpy.types.PropertyGroup):
    """Collection of sequences for a single rig."""
    armatureName: StringProperty(
        name="Armature"
    )  # type: ignore
    
    sequences: CollectionProperty(
        type=SequenceItem
    )  # type: ignore


# ============================================================================
# Registration
# ============================================================================

CLASSES = [
    SequenceItem,
    SequenceRigData,
]


def register():
    """Register all property groups in this module."""
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister all property groups in this module."""
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
