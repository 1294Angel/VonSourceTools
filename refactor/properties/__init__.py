"""
Properties module - Contains all Blender property groups.

Registration order is important:
1. qc_properties - Base property groups (VMT, Bodygroup, etc.)
2. sequence_properties - Sequence property groups (depends on some base types)
3. toolbox_properties - Main property groups (depends on all above)
"""
from . import qc_properties
from . import sequence_properties
from . import toolbox_properties

# Order matters for registration
MODULES = [
    qc_properties,
    sequence_properties,
    toolbox_properties,
]


def register():
    """Register all property groups in the correct order."""
    for module in MODULES:
        module.register()


def unregister():
    """Unregister all property groups in reverse order."""
    for module in reversed(MODULES):
        module.unregister()
