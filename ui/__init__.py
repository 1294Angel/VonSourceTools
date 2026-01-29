"""
UI module - Contains all Blender UI panels for VonSourceTools.

Each panel section is in its own file for better organization:
- parent_panel.py: Main parent panel
- qc_panels.py: QC Generator panels
- delta_anim_panels.py: Delta animation panels
- vmt_generator_panels.py: VMT/Material to VTF panels
- image_converter_panel.py: Image converter panel
- smd_export_panel.py: SMD export panel
"""
from . import parent_panel
from . import qc_panels
from . import delta_anim_panels
from . import vmt_generator_panels
from . import image_converter_panel
from . import smd_export_panel

# Registration order matters - parent panel must be first
MODULES = [
    parent_panel,
    qc_panels,
    delta_anim_panels,
    vmt_generator_panels,
    image_converter_panel,
    smd_export_panel,
]


def register():
    """Register all UI panels."""
    for module in MODULES:
        module.register()


def unregister():
    """Unregister all UI panels."""
    for module in reversed(MODULES):
        module.unregister()
