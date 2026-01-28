"""
Property groups for animation sequence data.
"""
import json
import bpy  # type: ignore
from bpy.props import (
    StringProperty, BoolProperty, EnumProperty,
    CollectionProperty
)
from pathlib import Path

from ..data.constants import MODEL_TYPE_CATEGORY_MAP, NONE_ENUM


def activity_item_items(self, context):
    """Generate activity items based on selected category."""
    none_enum = ("NONE", "None", "Do not replace any activity")
    
    toolbox = context.scene.toolBox
    json_path = Path(toolbox.string_activityfilelocation)
    
    if not json_path.is_file():
        return [none_enum]
    
    with json_path.open("r", encoding="utf-8") as f:
        activities_data = json.load(f)
    
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
    
    toolbox = context.scene.toolBox
    json_path = Path(toolbox.string_activityfilelocation)
    
    if not json_path.is_file():
        return [none_enum]
    
    with json_path.open("r", encoding="utf-8") as f:
        activities_data = json.load(f)
    
    model_type = toolbox.enum_qcGen_modelType
    allowed = MODEL_TYPE_CATEGORY_MAP.get(model_type, [])
    
    items = [
        (cat, cat.replace("_", " "), f"Activity category: {cat}")
        for cat in activities_data.keys()
        if cat in allowed
    ]
    
    return [none_enum] + items if items else [none_enum]


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


# Registration
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
