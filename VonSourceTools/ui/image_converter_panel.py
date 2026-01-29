"""
Image Converter Panel for VonSourceTools.
"""
import bpy  # type: ignore


# ============================================================================
# Image Converter Panel
# ============================================================================

class VON_PT_image_converter(bpy.types.Panel):
    """Image filetype converter panel"""
    bl_idname = "VON_PT_image_converter"
    bl_label = "Image Filetype Converter"
    bl_parent_id = "VON_PT_parent"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        from ..data.paths import get_vtfcmd_path
        
        layout = self.layout
        scene = context.scene
        img_converter = scene.von_image_converter
        
        layout.label(text="Image Filetype Converter")
        
        # VTFCmd path status
        vtfcmd_path = get_vtfcmd_path()
        if vtfcmd_path:
            layout.label(text="✓ VTFCmd: Found", icon='CHECKMARK')
        else:
            layout.label(text="VTFCmd: Not found", icon='ERROR')
            layout.prop(img_converter, "string_vtfcmdPath", text="VTFCmd Path")
            layout.label(text="Place VTFCmd.exe in addon's storeditems/external_software_dependancies/vtfcmd/ folder", icon='INFO')
        
        layout.separator()
        
        row = layout.row()
        row.prop(img_converter, "string_inputFolder", text="Input Folder")
        row.prop(img_converter, "string_outputFolder", text="Output Folder")
        
        row = layout.row()
        row.prop(img_converter, "enum_sourceFiletype", text="Source Filetype")
        row.prop(img_converter, "enum_targetFiletype", text="Target Filetype")
        
        layout.operator("von.batchconvertfiletypes", text="Run Conversion")


# ============================================================================
# Registration
# ============================================================================

CLASSES = [
    VON_PT_image_converter,
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
