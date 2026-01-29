"""
Operators for StudioMDL compilation functionality.
"""
import bpy  # type: ignore

from ..core.studiomdl import run_definebones_from_context


class VONSTUDIOMDL_OT_run_definebones(bpy.types.Operator):
    """Run studiomdl with -definebones flag"""
    bl_idname = "von.run_definebones_vondata"
    bl_label = "Run Define Bones"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        toolbox = scene.toolBox
        
        try:
            stdout, stderr = run_definebones_from_context(context)
            self.report({'INFO'}, "Define Bones completed. Check console for output.")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}


# Registration
CLASSES = [
    VONSTUDIOMDL_OT_run_definebones,
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
