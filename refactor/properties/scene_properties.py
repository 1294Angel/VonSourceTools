"""
Scene property registration.

This module registers all property groups to the Blender scene.
It serves as the central point for attaching settings from all panels
to bpy.types.Scene.
"""
import bpy  # type: ignore
from bpy.props import PointerProperty, CollectionProperty, IntProperty

from .qc_generator_properties import QC_PrimaryData, QCGeneratorSettings
from .delta_anim_properties import DeltaAnimSettings
from .image_converter_properties import ImageConverterSettings
from .smd_export_properties import SMDExportSettings
from .sequence_properties import SequenceRigData


def register_scene_properties():
    """Register all property groups to the scene."""
    
    # QC Generator
    bpy.types.Scene.von_qc_data = PointerProperty(type=QC_PrimaryData)
    bpy.types.Scene.von_qc_settings = PointerProperty(type=QCGeneratorSettings)
    
    # Add sequence data to QC data (done after registration)
    # This is handled via CollectionProperty in QC_PrimaryData
    
    # Delta Animation
    bpy.types.Scene.von_delta_anim = PointerProperty(type=DeltaAnimSettings)
    
    # Image Converter
    bpy.types.Scene.von_image_converter = PointerProperty(type=ImageConverterSettings)
    
    # SMD Export
    bpy.types.Scene.von_smd_export = PointerProperty(type=SMDExportSettings)
    
    # Sequence data index for UI lists
    bpy.types.Scene.von_sequence_index = IntProperty(default=0)


def unregister_scene_properties():
    """Unregister all scene properties."""
    properties_to_remove = [
        'von_qc_data',
        'von_qc_settings',
        'von_delta_anim',
        'von_image_converter',
        'von_smd_export',
        'von_sequence_index',
    ]
    
    for prop_name in properties_to_remove:
        if hasattr(bpy.types.Scene, prop_name):
            try:
                delattr(bpy.types.Scene, prop_name)
            except Exception as e:
                print(f"Warning: Could not remove property {prop_name}: {e}")


def register():
    """Register scene properties."""
    register_scene_properties()


def unregister():
    """Unregister scene properties."""
    unregister_scene_properties()
