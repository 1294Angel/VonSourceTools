"""
Operators for QC file generation.
"""
import bpy  # type: ignore

from ..core.qc_builder import generate_qc_file, gather_qc_data_from_scene, build_qc_content, write_qc_file_from_data
from ..core.sequences import populate_sequence_data
from ..properties.qc_generator_properties import sync_bodygroup_boxes
from ..utils.threading_utils import (
    run_in_background,
    get_task_result,
    is_task_finished,
    cleanup_task,
    TaskStatus,
)


def _qc_generation_task(qc_data):
    """
    Background task function for QC file generation.
    
    This runs in a separate thread to avoid blocking Blender.
    """
    output_path = write_qc_file_from_data(qc_data)
    return {
        'output_path': output_path,
        'model_type': qc_data.model_type,
        'model_name': qc_data.model_name,
    }


class VONQC_OT_generate_prop(bpy.types.Operator):
    """Generate QC file for a prop model (threaded)"""
    bl_idname = "von.qcgenerator_prop"
    bl_label = "Generate Prop QC"
    bl_description = "Generate a QC file for a static prop model"
    bl_options = {'REGISTER'}
    
    _timer = None
    _task_id = None
    
    @classmethod
    def poll(cls, context):
        """Check if operator can run."""
        qc_settings = context.scene.von_qc_settings
        return (qc_settings.string_outputPath != "" and 
                qc_settings.string_mdlModelName != "")
    
    def execute(self, context):
        try:
            # Gather data on main thread (accesses Blender data)
            qc_data = gather_qc_data_from_scene(context)
            
            # Start background task for file writing
            self._task_id = run_in_background(_qc_generation_task, qc_data)
            
            # Set up modal timer
            wm = context.window_manager
            self._timer = wm.event_timer_add(0.1, window=context.window)
            wm.modal_handler_add(self)
            
            self.report({'INFO'}, "Generating QC file...")
            return {'RUNNING_MODAL'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to gather QC data: {str(e)}")
            return {'CANCELLED'}
    
    def modal(self, context, event):
        if event.type == 'TIMER':
            if is_task_finished(self._task_id):
                return self._finish(context)
        return {'PASS_THROUGH'}
    
    def _finish(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        
        result = get_task_result(self._task_id)
        cleanup_task(self._task_id)
        
        if result is None or result.status == TaskStatus.FAILED:
            error = result.error if result else "Unknown error"
            self.report({'ERROR'}, f"Failed to generate QC: {error}")
            return {'CANCELLED'}
        
        task_result = result.result
        self.report({'INFO'}, f"QC file generated: {task_result['output_path']}")
        return {'FINISHED'}
    
    def cancel(self, context):
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
        if self._task_id:
            cleanup_task(self._task_id)


class VONQC_OT_generate_character(bpy.types.Operator):
    """Generate QC file for a character model (threaded)"""
    bl_idname = "von.qcgenerator_character"
    bl_label = "Generate Character QC"
    bl_description = "Generate a QC file for a character/player model"
    bl_options = {'REGISTER'}
    
    _timer = None
    _task_id = None
    
    @classmethod
    def poll(cls, context):
        qc_settings = context.scene.von_qc_settings
        return (qc_settings.string_outputPath != "" and 
                qc_settings.string_mdlModelName != "")
    
    def execute(self, context):
        try:
            qc_data = gather_qc_data_from_scene(context)
            self._task_id = run_in_background(_qc_generation_task, qc_data)
            
            wm = context.window_manager
            self._timer = wm.event_timer_add(0.1, window=context.window)
            wm.modal_handler_add(self)
            
            self.report({'INFO'}, "Generating QC file...")
            return {'RUNNING_MODAL'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to gather QC data: {str(e)}")
            return {'CANCELLED'}
    
    def modal(self, context, event):
        if event.type == 'TIMER':
            if is_task_finished(self._task_id):
                return self._finish(context)
        return {'PASS_THROUGH'}
    
    def _finish(self, context):
        context.window_manager.event_timer_remove(self._timer)
        result = get_task_result(self._task_id)
        cleanup_task(self._task_id)
        
        if result is None or result.status == TaskStatus.FAILED:
            self.report({'ERROR'}, f"Failed to generate QC: {result.error if result else 'Unknown'}")
            return {'CANCELLED'}
        
        self.report({'INFO'}, f"QC file generated: {result.result['output_path']}")
        return {'FINISHED'}
    
    def cancel(self, context):
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
        if self._task_id:
            cleanup_task(self._task_id)


class VONQC_OT_generate_npc(bpy.types.Operator):
    """Generate QC file for an NPC model (threaded)"""
    bl_idname = "von.qcgenerator_npc"
    bl_label = "Generate NPC QC"
    bl_description = "Generate a QC file for an NPC model"
    bl_options = {'REGISTER'}
    
    _timer = None
    _task_id = None
    
    @classmethod
    def poll(cls, context):
        qc_settings = context.scene.von_qc_settings
        return (qc_settings.string_outputPath != "" and 
                qc_settings.string_mdlModelName != "")
    
    def execute(self, context):
        try:
            qc_data = gather_qc_data_from_scene(context)
            self._task_id = run_in_background(_qc_generation_task, qc_data)
            
            wm = context.window_manager
            self._timer = wm.event_timer_add(0.1, window=context.window)
            wm.modal_handler_add(self)
            
            self.report({'INFO'}, "Generating QC file...")
            return {'RUNNING_MODAL'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to gather QC data: {str(e)}")
            return {'CANCELLED'}
    
    def modal(self, context, event):
        if event.type == 'TIMER':
            if is_task_finished(self._task_id):
                return self._finish(context)
        return {'PASS_THROUGH'}
    
    def _finish(self, context):
        context.window_manager.event_timer_remove(self._timer)
        result = get_task_result(self._task_id)
        cleanup_task(self._task_id)
        
        if result is None or result.status == TaskStatus.FAILED:
            self.report({'ERROR'}, f"Failed to generate QC: {result.error if result else 'Unknown'}")
            return {'CANCELLED'}
        
        self.report({'INFO'}, f"QC file generated: {result.result['output_path']}")
        return {'FINISHED'}
    
    def cancel(self, context):
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
        if self._task_id:
            cleanup_task(self._task_id)


class VONQC_OT_generate_viewmodel(bpy.types.Operator):
    """Generate QC file for a viewmodel (threaded)"""
    bl_idname = "von.qcgenerator_viewmodel"
    bl_label = "Generate Viewmodel QC"
    bl_description = "Generate a QC file for a first-person viewmodel"
    bl_options = {'REGISTER'}
    
    _timer = None
    _task_id = None
    
    @classmethod
    def poll(cls, context):
        qc_settings = context.scene.von_qc_settings
        return (qc_settings.string_outputPath != "" and 
                qc_settings.string_mdlModelName != "")
    
    def execute(self, context):
        try:
            qc_data = gather_qc_data_from_scene(context)
            self._task_id = run_in_background(_qc_generation_task, qc_data)
            
            wm = context.window_manager
            self._timer = wm.event_timer_add(0.1, window=context.window)
            wm.modal_handler_add(self)
            
            self.report({'INFO'}, "Generating QC file...")
            return {'RUNNING_MODAL'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to gather QC data: {str(e)}")
            return {'CANCELLED'}
    
    def modal(self, context, event):
        if event.type == 'TIMER':
            if is_task_finished(self._task_id):
                return self._finish(context)
        return {'PASS_THROUGH'}
    
    def _finish(self, context):
        context.window_manager.event_timer_remove(self._timer)
        result = get_task_result(self._task_id)
        cleanup_task(self._task_id)
        
        if result is None or result.status == TaskStatus.FAILED:
            self.report({'ERROR'}, f"Failed to generate QC: {result.error if result else 'Unknown'}")
            return {'CANCELLED'}
        
        self.report({'INFO'}, f"QC file generated: {result.result['output_path']}")
        return {'FINISHED'}
    
    def cancel(self, context):
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
        if self._task_id:
            cleanup_task(self._task_id)


class VONQC_OT_generate_worldmodel(bpy.types.Operator):
    """Generate QC file for a worldmodel (threaded)"""
    bl_idname = "von.qcgenerator_worldmodel"
    bl_label = "Generate Worldmodel QC"
    bl_description = "Generate a QC file for a third-person worldmodel"
    bl_options = {'REGISTER'}
    
    _timer = None
    _task_id = None
    
    @classmethod
    def poll(cls, context):
        qc_settings = context.scene.von_qc_settings
        return (qc_settings.string_outputPath != "" and 
                qc_settings.string_mdlModelName != "")
    
    def execute(self, context):
        try:
            qc_data = gather_qc_data_from_scene(context)
            self._task_id = run_in_background(_qc_generation_task, qc_data)
            
            wm = context.window_manager
            self._timer = wm.event_timer_add(0.1, window=context.window)
            wm.modal_handler_add(self)
            
            self.report({'INFO'}, "Generating QC file...")
            return {'RUNNING_MODAL'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to gather QC data: {str(e)}")
            return {'CANCELLED'}
    
    def modal(self, context, event):
        if event.type == 'TIMER':
            if is_task_finished(self._task_id):
                return self._finish(context)
        return {'PASS_THROUGH'}
    
    def _finish(self, context):
        context.window_manager.event_timer_remove(self._timer)
        result = get_task_result(self._task_id)
        cleanup_task(self._task_id)
        
        if result is None or result.status == TaskStatus.FAILED:
            self.report({'ERROR'}, f"Failed to generate QC: {result.error if result else 'Unknown'}")
            return {'CANCELLED'}
        
        self.report({'INFO'}, f"QC file generated: {result.result['output_path']}")
        return {'FINISHED'}
    
    def cancel(self, context):
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
        if self._task_id:
            cleanup_task(self._task_id)


class VONQC_OT_refresh_collections(bpy.types.Operator):
    """Refresh the collection list for bodygroups"""
    bl_idname = "von.qcgenerator_refresh_collections"
    bl_label = "Refresh Collections"
    bl_description = "Refresh the list of available collections for bodygroups"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        sync_bodygroup_boxes(scene)
        self.report({'INFO'}, "Collections synced with scene.")
        return {'FINISHED'}


class VONQC_OT_collect_sequences(bpy.types.Operator):
    """Collect animation sequences from selected armatures"""
    bl_idname = "von.collect_sequences"
    bl_label = "Collect Sequences"
    bl_description = "Collect animation sequences from selected armatures"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return any(obj.type == 'ARMATURE' for obj in context.selected_objects)
    
    def execute(self, context):
        populate_sequence_data(context)
        self.report({'INFO'}, "Sequences collected from selected armatures")
        return {'FINISHED'}


class VONQC_OT_preview_qc(bpy.types.Operator):
    """Preview the QC file that would be generated"""
    bl_idname = "von.qcgenerator_preview"
    bl_label = "Preview QC"
    bl_description = "Preview the QC content without writing to file"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        try:
            qc_data = gather_qc_data_from_scene(context)
            content = build_qc_content(qc_data)
            
            # Print to console
            print("\n" + "=" * 60)
            print("QC PREVIEW")
            print("=" * 60)
            print(content)
            print("=" * 60 + "\n")
            
            self.report({'INFO'}, "QC preview printed to console (Window > Toggle System Console)")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to generate preview: {str(e)}")
            return {'CANCELLED'}


# Registration
CLASSES = [
    VONQC_OT_generate_prop,
    VONQC_OT_generate_character,
    VONQC_OT_generate_npc,
    VONQC_OT_generate_viewmodel,
    VONQC_OT_generate_worldmodel,
    VONQC_OT_refresh_collections,
    VONQC_OT_collect_sequences,
    VONQC_OT_preview_qc,
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
