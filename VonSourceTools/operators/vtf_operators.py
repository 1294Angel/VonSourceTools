"""
Operators for VTF batch conversion functionality.
"""
import bpy  # type: ignore

from ..core.vtf_conversion import batch_convert, batch_convert_files
from ..utils.threading_utils import (
    run_in_background,
    get_task_result,
    is_task_finished,
    cleanup_task,
    TaskStatus,
)


class VONVTF_OT_batch_convert(bpy.types.Operator):
    """Batch convert image files to/from VTF format (threaded)"""
    bl_idname = "von.batchconvertfiletypes"
    bl_label = "Convert Filetypes"
    bl_options = {'REGISTER'}
    
    # Modal state
    _timer = None
    _task_id = None
    
    @classmethod
    def poll(cls, context):
        """Check if operator can run."""
        from ..data.paths import get_vtfcmd_path
        
        img_converter = context.scene.von_image_converter
        
        # Check input/output folders are set
        if not img_converter.string_inputFolder:
            return False
        if not img_converter.string_outputFolder:
            return False
        
        # Check VTFCmd is available
        bundled_vtfcmd = get_vtfcmd_path()
        if bundled_vtfcmd is not None:
            return True
        
        return img_converter.string_vtfcmdPath != ""
    
    def execute(self, context):
        """Start the batch conversion process."""
        from ..data.paths import get_vtfcmd_path
        
        scene = context.scene
        img_converter = scene.von_image_converter
        
        # Get VTFCmd path
        bundled_vtfcmd = get_vtfcmd_path()
        if bundled_vtfcmd is not None:
            vtfcmd_exe = str(bundled_vtfcmd)
        else:
            vtfcmd_exe = img_converter.string_vtfcmdPath
        
        # Start background task
        self._task_id = run_in_background(
            batch_convert_files,
            vtfcmd_exe,
            img_converter.string_inputFolder,
            img_converter.string_outputFolder,
            img_converter.enum_sourceFiletype,
            img_converter.enum_targetFiletype
        )
        
        # Set up modal timer
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        
        self.report({'INFO'}, "Batch conversion started in background...")
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        """Check task completion."""
        if event.type == 'TIMER':
            if is_task_finished(self._task_id):
                return self._finish(context)
        
        return {'PASS_THROUGH'}
    
    def _finish(self, context):
        """Handle task completion."""
        # Remove timer
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        
        # Get result
        result = get_task_result(self._task_id)
        cleanup_task(self._task_id)
        
        if result is None:
            self.report({'ERROR'}, "Task result not found")
            return {'CANCELLED'}
        
        if result.status == TaskStatus.FAILED:
            self.report({'ERROR'}, f"Batch conversion failed: {result.error}")
            return {'CANCELLED'}
        
        if result.status == TaskStatus.CANCELLED:
            self.report({'WARNING'}, "Batch conversion was cancelled")
            return {'CANCELLED'}
        
        # Process successful result
        task_result = result.result
        
        if task_result.get('error'):
            self.report({'ERROR'}, task_result['error'])
            return {'CANCELLED'}
        
        success = task_result['success']
        failed = task_result['failed']
        
        if success > 0 or failed > 0:
            self.report(
                {'INFO'},
                f"Conversion complete. Success: {success}, Failed: {failed}"
            )
        else:
            self.report({'WARNING'}, "No files were converted")
        
        return {'FINISHED'}
    
    def cancel(self, context):
        """Handle operator cancellation."""
        if self._timer:
            wm = context.window_manager
            wm.event_timer_remove(self._timer)
        if self._task_id:
            cleanup_task(self._task_id)


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
