"""
Properties module - Contains all Blender property groups.

Organized by panel/dropdown menu:
- qc_generator_properties: QC Generator panel
- delta_anim_properties: Delta Animation Trick panel
- material_vtf_properties: Material to VTF Converter panel
- image_converter_properties: Image Filetype Converter panel
- smd_export_properties: Batch SMD Export panel
- sequence_properties: Animation sequence sub-properties
- scene_properties: Central scene property registration
- toolbox_properties: Legacy backwards-compatible properties

Registration order is important - base types must be registered
before property groups that reference them.
"""
from . import sequence_properties
from . import qc_generator_properties
from . import delta_anim_properties
from . import material_vtf_properties
from . import image_converter_properties
from . import smd_export_properties
from . import scene_properties
from . import toolbox_properties

# Legacy imports for backwards compatibility
from .qc_generator_properties import (
    QC_PrimaryData,
    QCGeneratorSettings,
    VMT_FilePathItem,
    BodygroupBox,
    BodygroupCollectionItem,
    ArmatureName,
    BoneNameForAttach,
    sync_bodygroup_boxes,
    get_bodygroup_by_name,
    surfaceprop_category_items_callback,
    surfaceprop_item_items_callback,
)
from .toolbox_properties import VonToolbox
from .delta_anim_properties import DeltaAnimSettings
from .image_converter_properties import ImageConverterSettings
from .smd_export_properties import SMDExportSettings
from .sequence_properties import SequenceItem, SequenceRigData
from .material_vtf_properties import (
    VMT_Parameters,
    VMT_MaterialListItem,
    VMT_PathSettings,
)

# Order matters for registration
MODULES = [
    sequence_properties,        # Base sequence types
    qc_generator_properties,    # QC Generator (depends on sequence)
    delta_anim_properties,      # Delta Animation Trick
    material_vtf_properties,    # Material to VTF Converter
    image_converter_properties, # Image Filetype Converter
    smd_export_properties,      # Batch SMD Export
    toolbox_properties,         # Legacy properties (depends on above)
    scene_properties,           # Scene registration (must be last)
]


def register():
    """Register all property groups in the correct order."""
    for module in MODULES:
        module.register()


def unregister():
    """Unregister all property groups in reverse order."""
    for module in reversed(MODULES):
        module.unregister()
