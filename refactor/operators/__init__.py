"""
Operators module - Contains all Blender operators for VonSourceTools.
"""
from . import delta_anim_operators
from . import qc_operators
from . import smd_operators
from . import vtf_operators
from . import studiomdl_operators

MODULES = [
    delta_anim_operators,
    qc_operators,
    smd_operators,
    vtf_operators,
    studiomdl_operators,
]


def register():
    """Register all operators."""
    for module in MODULES:
        module.register()


def unregister():
    """Unregister all operators."""
    for module in reversed(MODULES):
        module.unregister()
