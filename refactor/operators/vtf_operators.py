"""
Operators for VTF batch conversion functionality.
"""
import bpy  # type: ignore

from ..core.vtf_conversion import batch_convert


class VONVTF_OT_batch_convert(bpy.types.Operator):
    """Batch convert image files to/from VTF format"""
    bl_idname = "von.batchconvertfiletypes"
    bl_label = "Convert Filetypes"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        toolbox = scene.toolBox
        
        success, failed = batch_convert(context)
        
        if success > 0 or failed > 0:
            self.report(
                {'INFO'},
                f"Conversion complete. Success: {success}, Failed: {failed}"
            )
        else:
            self.report({'WARNING'}, "No files were converted")
        
        return {'FINISHED'}


# Registration
CLASSES = [
    VONVTF_OT_batch_convert,
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
