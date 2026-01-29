"""
Operators for SMD batch export functionality.
"""
import os
import bpy  # type: ignore

from ..core.smd_export import (
    split_objects_into_collections,
    restore_objects_from_collections,
    export_scene_smd,
)


class VONSMD_OT_split_objects(bpy.types.Operator):
    """Split all objects into temporary collections"""
    bl_idname = "object.split_objects"
    bl_label = "Split Objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        split_objects_into_collections(context)
        self.report({'INFO'}, "Objects split into temporary collections.")
        return {'FINISHED'}


class VONSMD_OT_restore_objects(bpy.types.Operator):
    """Restore objects to their original collections"""
    bl_idname = "object.restore_objects"
    bl_label = "Restore Objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        restore_objects_from_collections(context)
        self.report({'INFO'}, "Objects restored to original collections.")
        return {'FINISHED'}


class VONSMD_OT_export(bpy.types.Operator):
    """Export scene to SMD format"""
    bl_idname = "object.export_smd"
    bl_label = "Export Scene"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        smd_export = scene.von_smd_export
        export_folder = smd_export.string_exportFolder
        
        if not os.path.exists(export_folder):
            os.makedirs(export_folder)
        
        # Select all objects for export
        for obj in context.scene.objects:
            obj.select_set(True)
        
        try:
            bpy.ops.export_scene.smd('INVOKE_DEFAULT')
            self.report({'INFO'}, "Export started. Choose folder in the popup.")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {e}")
            return {'CANCELLED'}


# Registration
CLASSES = [
    VONSMD_OT_split_objects,
    VONSMD_OT_restore_objects,
    VONSMD_OT_export,
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
