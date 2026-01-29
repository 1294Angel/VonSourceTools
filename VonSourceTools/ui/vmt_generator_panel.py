import bpy # type: ignore
# ============================================================================
# VMT Generator Panel
# ============================================================================

class VON_PT_vmt_generator(bpy.types.Panel):
    """VMT Generator panel"""
    bl_idname = "VON_PT_vmt_generator"
    bl_label = "VMT Generator Main"
    bl_parent_id = "VON_PT_parent"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="VMT Generator")

# ============================================================================
# Registration
# ============================================================================

CLASSES = [
    # Other panels
    VON_PT_vmt_generator,
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
