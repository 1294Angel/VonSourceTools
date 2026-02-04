import bpy # type: ignore
from bpy.props import * # type: ignore

class TextureAtlasSettings(bpy.types.PropertyGroup):
    atlas_size: bpy.props.IntProperty(
        name="Atlas Size",
        description="Size of each atlas sheet generated, system will generate multiple if all existing textures don't fit in the given atlas resolution",
        default = 4096
        )# type: ignore
    atlas_output_path: bpy.props.StringProperty(
        name = "Atlas Export Filepath",
        description = "Where will the generated atlas/'s be stored on your device?",
        default = "",
        subtype = "FILE_PATH"
    )# type: ignore
    atlas_simplepack = bpy.props.BoolProperty(
        name="Simple Packing?",
        description="Packs the materials in a simple, rapid way. Turn off for complex packing. (NOT WORKING ATM)",
        default=True,
    )# type: ignore
    atlas_moveUVs: bpy.props.BoolProperty(
        name="Move UV's?",
        description="Move the object's UV's to match the new locations of the newly created atlas trimsheet.",
        default=True,
    )# type: ignore
    atlas_applymaterial: bpy.props.BoolProperty(
        name="Apply Material?",
        description="Remove all old materials and replace them with the new trimsheet material.",
        default=True,
    )# type: ignore
    atlas_materialname: bpy.props.StringProperty(
        name = "Atlas Material Name",
        description = "What will the atlas material be called?",
        default = "atlas_material",
        maxlen = 100
    )# type: ignore
    atlas_single_atlas: bpy.props.BoolProperty(
        name="Single Atlas?",
        description="Only create a single atlas material. Downsizing any texture files that do not fit within the atlas size.",
        default=False,
    )# type: ignore
    atlas_resize_oversized: bpy.props.BoolProperty(
        name="Single Atlas?",
        description="Only create a single atlas material. Downsizing any texture files that do not fit within the atlas size.",
        default=False,
    )# type: ignore
    atlas_crop_transparent: bpy.props.BoolProperty(
        name="Single Atlas?",
        description="Only create a single atlas material. Downsizing any texture files that do not fit within the atlas size.",
        default=False,
    )# type: ignore
    
class texture_atlas_material_item(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()# type: ignore
    doWork: bpy.props.BoolProperty(name="Include", default=True)# type: ignore

class texture_atlas_mesh_item(bpy.types.PropertyGroup):
    meshName: bpy.props.StringProperty()# type: ignore
    materials: bpy.props.CollectionProperty(type=texture_atlas_material_item)# type: ignore



# ============================================================================
# Registration
# ============================================================================

CLASSES = [
    TextureAtlasSettings,
    texture_atlas_material_item,
    texture_atlas_mesh_item,
]


def register():
    """Register all property groups in this module."""
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister all property groups in this module."""
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)