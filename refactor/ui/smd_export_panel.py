"""
SMD Export Panel for VonSourceTools.
"""
import bpy  # type: ignore


# ============================================================================
# SMD Export Panel
# ============================================================================

class VON_PT_smd_export(bpy.types.Panel):
    """Batch SMD export panel"""
    bl_idname = "VON_PT_smd_export"
    bl_label = "Batch SMD Export"
    bl_parent_id = "VON_PT_parent"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scene = context.scene
        toolbox = scene.toolBox
        layout = self.layout
        
        layout.label(text="Collections:")
        layout.operator("object.split_objects", icon='OUTLINER_OB_GROUP_INSTANCE')
        layout.operator("object.restore_objects", icon='FILE_REFRESH')
        
        layout.separator()
        
        layout.label(text="Export:")
        layout.prop(toolbox, "string_export_folder", text="Folder")
        layout.operator("object.export_smd", icon='EXPORT')


# ============================================================================
# Registration
# ============================================================================

CLASSES = [
    VON_PT_smd_export,
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
