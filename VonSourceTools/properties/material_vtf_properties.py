"""
Properties for Material to VTF conversion.

This module handles converting Blender materials to VTF format
and generating VMT files with advanced shader parameters.
"""
import bpy
from bpy.props import (
    StringProperty,
    BoolProperty,
    IntProperty,
    FloatProperty,
    FloatVectorProperty,
    PointerProperty,
    CollectionProperty,
    EnumProperty
)
from bpy.types import PropertyGroup


# ============================================================================
# VMT Parameters Property Group
# ============================================================================

class VMT_Parameters(PropertyGroup):
    """Property group for VMT material parameters."""
    
    # Texture maps
    normal_map: PointerProperty(
        type=bpy.types.Image,
        name="Normal Map",
        description="Select the normal map image for this material"
    )
    
    phong_exponent_map: PointerProperty(
        type=bpy.types.Image,
        name="Phong Exponent Map",
        description="Select the phong exponent texture (specular map)"
    )
    
    # Phong parameters
    enable_phong: BoolProperty(
        name="Enable Phong",
        description="Enable phong shading",
        default=True
    )
    
    phong_boost: FloatProperty(
        name="Phong Boost",
        description="Phong reflection intensity",
        default=1.0,
        min=0.0,
        max=10.0
    )
    
    phong_albedo_tint: BoolProperty(
        name="Phong Albedo Tint",
        description="Tint phong reflections with base texture color",
        default=True
    )
    
    phong_albedo_boost: FloatProperty(
        name="Phong Albedo Boost",
        description="Boost phong albedo tinting",
        default=50.0,
        min=0.0,
        max=100.0
    )
    
    phong_fresnel_ranges: FloatVectorProperty(
        name="Phong Fresnel Ranges",
        description="Fresnel ranges for phong reflections [min, mid, max]",
        default=(1.0, 0.1, 0.0),
        size=3,
        min=0.0,
        max=1.0
    )
    
    # Rim lighting
    enable_rimlight: BoolProperty(
        name="Enable Rim Light",
        description="Enable rim lighting effect",
        default=True
    )
    
    rimlight_exponent: FloatProperty(
        name="Rim Light Exponent",
        description="Controls the falloff of rim lighting",
        default=100.0,
        min=0.1,
        max=1000.0
    )
    
    rimlight_boost: FloatProperty(
        name="Rim Light Boost",
        description="Intensity of rim lighting",
        default=1.0,
        min=0.0,
        max=10.0
    )
    
    rim_mask: BoolProperty(
        name="Rim Mask",
        description="Use rim masking",
        default=True
    )
    
    # Environment mapping
    enable_envmap: BoolProperty(
        name="Enable Environment Map",
        description="Enable environment mapping (reflections)",
        default=True
    )
    
    envmap_tint: FloatVectorProperty(
        name="Environment Map Tint",
        description="Tint color for environment reflections",
        default=(0.11, 0.106, 0.106),
        size=3,
        min=0.0,
        max=1.0,
        subtype='COLOR'
    )
    
    # Advanced parameters
    normal_map_alpha_envmap_mask: BoolProperty(
        name="Normal Alpha Envmap Mask",
        description="Use normal map alpha as environment map mask",
        default=True
    )
    
    color2: FloatVectorProperty(
        name="Color2",
        description="Secondary color (usually kept at [0,0,0])",
        default=(0.0, 0.0, 0.0),
        size=3,
        min=0.0,
        max=1.0,
        subtype='COLOR'
    )
    
    blend_tint_by_base_alpha: BoolProperty(
        name="Blend Tint By Base Alpha",
        description="Blend tint using base texture alpha",
        default=True
    )


# ============================================================================
# Material List Item
# ============================================================================

class VMT_MaterialListItem(PropertyGroup):
    """Property group for individual materials in the conversion list."""
    
    material_checkbox: BoolProperty(
        name="Select",
        description="Select this material for processing",
        default=True
    )
    
    material_name: StringProperty(
        name="Material Name",
        description="Name of the material",
        default=""
    )
    
    material: PointerProperty(
        type=bpy.types.Material,
        name="Material",
        description="Reference to the Blender material"
    )
    
    # VMT parameters for this specific material
    vmt_params: PointerProperty(
        type=VMT_Parameters,
        name="VMT Parameters",
        description="VMT generation parameters for this material"
    )


# ============================================================================
# Path Settings
# ============================================================================

class VMT_PathSettings(PropertyGroup):
    """Property group for path settings."""
    
    path: StringProperty(
        name="Path",
        description="Path to directory or file",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
    )


# ============================================================================
# Scene Properties Registration
# ============================================================================

def register_scene_properties():
    """Register custom scene properties for material VTF conversion."""
    
    # Material collection and index
    bpy.types.Scene.von_mats_collection = CollectionProperty(type=VMT_MaterialListItem)
    bpy.types.Scene.von_mats_index = IntProperty(default=0)
    
    # Path properties
    bpy.types.Scene.von_vtfcmd_path = PointerProperty(type=VMT_PathSettings)
    bpy.types.Scene.von_material_output_path = PointerProperty(type=VMT_PathSettings)
    
    # Boolean properties
    bpy.types.Scene.von_vtf_resize_bool = BoolProperty(
        name="Resize Images",
        description="Enable image resizing during conversion",
        default=False
    )
    
    bpy.types.Scene.von_vmt_generate_bool = BoolProperty(
        name="Generate VMT",
        description="Generate VMT material files alongside VTF textures",
        default=False
    )
    
    bpy.types.Scene.von_vmt_param_additive = BoolProperty(
        name="Additive",
        description="Enable additive blending in VMT",
        default=False
    )
    
    bpy.types.Scene.von_vmt_param_translucent = BoolProperty(
        name="Translucent",
        description="Enable translucent rendering in VMT",
        default=False
    )
    
    bpy.types.Scene.von_vmt_param_nocull = BoolProperty(
        name="No Cull",
        description="Disable backface culling in VMT",
        default=False
    )

    # Enum properties
    bpy.types.Scene.von_vtf_clamp_size = EnumProperty(
        name="Clamp Size",
        description="Maximum texture dimensions for VTF",
        items=[
            ('2x2', "2x2", "Very small texture size"),
            ('4x4', "4x4", ""),
            ('8x8', "8x8", ""),
            ('16x16', "16x16", ""),
            ('32x32', "32x32", ""),
            ('64x64', "64x64", ""),
            ('128x128', "128x128", ""),
            ('256x256', "256x256", "Standard texture size"),
            ('512x512', "512x512", "High resolution texture"),
            ('1024x1024', "1024x1024", "Very high resolution"),
            ('2048x2048', "2048x2048", "Maximum recommended size"),
            ('4096x4096', "4096x4096", "Ultra high resolution")
        ],
        default='512x512'
    )

    bpy.types.Scene.von_vtf_format = EnumProperty(
        name="Texture Format",
        description="VTF texture compression format",
        items=[
            ('dxt1', "DXT1", "Basic compression, no alpha channel"),
            ('dxt3', "DXT3", "Compression with explicit alpha"),
            ('dxt5', "DXT5", "Compression with interpolated alpha (recommended)")
        ],
        default='dxt5'
    )

    bpy.types.Scene.von_vtf_alpha_format = EnumProperty(
        name="Alpha Format",
        description="VTF alpha channel compression format",
        items=[
            ('dxt1', "DXT1", "Basic alpha compression"),
            ('dxt3', "DXT3", "Explicit alpha compression"),
            ('dxt5', "DXT5", "Interpolated alpha compression (recommended)")
        ],
        default='dxt5'
    )

    bpy.types.Scene.von_vtf_version = EnumProperty(
        name="VTF Version",
        description="VTF file format version",
        items=[
            ('7.2', "7.2", "Legacy version"),
            ('7.3', "7.3", "Standard version"),
            ('7.4', "7.4", "Enhanced features"),
            ('7.5', "7.5", "Latest version (recommended)")
        ],
        default='7.5'
    )

    bpy.types.Scene.von_vtf_resize_method = EnumProperty(
        name="Resize Method",
        description="Method for resizing images",
        items=[
            ('NEAREST', "Nearest", "Pixel art friendly, sharp edges"),
            ('BIGGEST', "Biggest", "Keep largest dimension"),
            ('SMALLEST', "Smallest", "Keep smallest dimension")
        ],
        default='BIGGEST'
    )

    bpy.types.Scene.von_vtf_resize_filter = EnumProperty(
        name="Resize Filter",
        description="Filter algorithm for image resizing",
        items=[
            ('TRIANGLE', "Triangle", "Smooth interpolation filter")
        ],
        default='TRIANGLE'
    )

    bpy.types.Scene.von_vmt_shader = EnumProperty(
        name="VMT Shader",
        description="Source Engine shader type for VMT files",
        items=[
            ('UnlitGeneric', "UnlitGeneric", "Basic unlit shader"),
            ('VertexlitGeneric', "VertexlitGeneric", "Vertex lighting (characters/props)"),
            ('LightmappedGeneric', "LightmappedGeneric", "Lightmap support (world geometry)")
        ],
        default='VertexlitGeneric'
    )


def unregister_scene_properties():
    """Unregister custom scene properties."""
    properties_to_remove = [
        'von_mats_collection', 'von_mats_index', 'von_vtfcmd_path', 
        'von_material_output_path', 'von_vtf_resize_bool', 'von_vtf_clamp_size',
        'von_vtf_resize_filter', 'von_vtf_resize_method', 'von_vtf_version',
        'von_vtf_alpha_format', 'von_vtf_format', 'von_vmt_generate_bool',
        'von_vmt_shader', 'von_vmt_param_additive', 'von_vmt_param_translucent',
        'von_vmt_param_nocull'
    ]
    
    for prop_name in properties_to_remove:
        if hasattr(bpy.types.Scene, prop_name):
            try:
                delattr(bpy.types.Scene, prop_name)
            except Exception as e:
                print(f"Warning: Could not remove property {prop_name}: {e}")


# ============================================================================
# Registration
# ============================================================================

CLASSES = [
    VMT_Parameters,
    VMT_MaterialListItem,
    VMT_PathSettings,
]


def register():
    """Register all classes and properties."""
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    register_scene_properties()


def unregister():
    """Unregister all classes and properties."""
    unregister_scene_properties()
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
