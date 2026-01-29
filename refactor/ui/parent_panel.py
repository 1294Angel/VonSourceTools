"""
Parent Panel for VonSourceTools.
"""
import bpy  # type: ignore


# ============================================================================
# Parent Panel
# ============================================================================

class VON_PT_parent(bpy.types.Panel):
    """Main parent panel for VonSourceTools"""
    bl_idname = "VON_PT_parent"
    bl_label = "Von Source Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw(self, context):
        layout = self.layout


# ============================================================================
# Registration
# ============================================================================

CLASSES = [
    VON_PT_parent,
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
