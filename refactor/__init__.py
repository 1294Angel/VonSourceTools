"""
VonSourceTools - Blender to Source Engine workflow addon
"""
import bpy # type: ignore

bl_info = {
    "name": "Vona's Blender Source Tools",
    "author": "Vona",
    "version": (0, 1, 0),  # Change from (0, 0, 2)
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > VonSourceTools",
    "description": "Streamline Blender to Source/Garry's Mod workflow with QC generation and delta animation tricks",
    "warning": "Early development - Expect bugs",
    "doc_url": "https://github.com/1294Angel/VonSourceTools#readme",
    "tracker_url": "https://github.com/1294Angel/VonSourceTools/issues",
    "category": "Import-Export",
}

# Import submodules
from . import properties
from . import operators
from . import ui

# Module list for registration
MODULES = [
    properties,
    operators,
    ui,
]

def register():
    """Register all addon components."""
    for module in MODULES:
        module.register()

def unregister():
    """Unregister all addon components."""
    for module in reversed(MODULES):
        module.unregister()

if __name__ == "__main__":
    register()