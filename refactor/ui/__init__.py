"""
UI module - Contains all Blender UI panels for VonSourceTools.
"""
from . import parent_panel
from . import delta_anim_panels
from . import image_converter_panel
from . import qc_panels
from . import smd_export_panel
from . import vmt_generator_panel

MODULES = [
    parent_panel,
    delta_anim_panels,
    image_converter_panel,
    qc_panels,
    smd_export_panel,
    vmt_generator_panel,
]


def register():
    """Register all UI panels."""
    for module in MODULES:
        module.register()


def unregister():
    """Unregister all UI panels."""
    for module in reversed(MODULES):
        module.unregister()
