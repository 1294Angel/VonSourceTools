"""
Property groups for QC generation data.
"""
import bpy  # type: ignore
from bpy.props import ( # type: ignore
    StringProperty, BoolProperty, IntProperty,
    CollectionProperty, PointerProperty
)


class VMT_FilePathItem(bpy.types.PropertyGroup):
    """Single VMT file path entry."""
    filepath: StringProperty(
        name="File Path",
        description="Path to VMT file",
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


# Registration
CLASSES = [
    VMT_FilePathItem,
    BodygroupCollectionItem,
    BodygroupBox,
    BoneNameForAttach,
    ArmatureName,
]


def register():
    """Register all property groups in this module."""
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister all property groups in this module."""
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
