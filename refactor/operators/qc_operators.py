"""
Operators for QC file generation.
"""
import bpy  # type: ignore

from ..core.qc_builder import write_qc_file
from ..core.sequences import populate_sequence_data
from ..properties.toolbox_properties import sync_bodygroup_boxes


class VONQC_OT_generate_prop(bpy.types.Operator):
    """Generate QC file for a prop model"""
    bl_idname = "von.qcgenerator_prop"
    bl_label = "Generate QC File"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        toolbox = scene.toolBox
        # TODO: Implement prop QC generation
        self.report({'INFO'}, "Prop QC generation not yet implemented")
        return {'FINISHED'}


class VONQC_OT_generate_character(bpy.types.Operator):
    """Generate QC file for a character model"""
    bl_idname = "von.qcgenerator_character"
    bl_label = "Generate QC File"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        toolbox = scene.toolBox
        # TODO: Implement character QC generation
        self.report({'INFO'}, "Character QC generation not yet implemented")
        return {'FINISHED'}


class VONQC_OT_generate_npc(bpy.types.Operator):
    """Generate QC file for an NPC model"""
    bl_idname = "von.qcgenerator_npc"
    bl_label = "Generate QC File"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        toolbox = scene.toolBox
        
        qc_commands = {
            "modelname": toolbox.string_qcGen_mdlModelName,
            "shouldGenCollis": toolbox.bool_qcGen_generateCollission,
            "includeanims": toolbox.enum_qcGen_charAnimIncludes
        }
        qc_controls = {
            "qc_output": toolbox.string_qcGen_outputPath
        }
        
        try:
            write_qc_file("npc", qc_commands, qc_controls)
            self.report({'INFO'}, "NPC QC file generated")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}


class VONQC_OT_generate_viewmodel(bpy.types.Operator):
    """Generate QC file for a viewmodel"""
    bl_idname = "von.qcgenerator_viewmodel"
    bl_label = "Generate QC File"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        self.report({'INFO'}, "Viewmodel QC generation not yet implemented")
        return {'FINISHED'}


class VONQC_OT_generate_worldmodel(bpy.types.Operator):
    """Generate QC file for a worldmodel"""
    bl_idname = "von.qcgenerator_worldmodel"
    bl_label = "Generate QC File"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        self.report({'INFO'}, "Worldmodel QC generation not yet implemented")
        return {'FINISHED'}


class VONQC_OT_refresh_collections(bpy.types.Operator):
    """Refresh the collection list for bodygroups"""
    bl_idname = "von.qcgenerator_refresh_collections"
    bl_label = "Refresh Collection List"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        sync_bodygroup_boxes(scene)
        self.report({'INFO'}, "Collections synced with scene.")
        return {'FINISHED'}


class VONQC_OT_collect_sequences(bpy.types.Operator):
    """Collect animation sequences from selected armatures"""
    bl_idname = "von.collect_sequences"
    bl_label = "Collect Animation Sequences"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return any(obj.type == 'ARMATURE' for obj in context.selected_objects)
    
    def execute(self, context):
        populate_sequence_data(context)
        self.report({'INFO'}, "Sequences collected from selected armatures")
        return {'FINISHED'}


# Registration
CLASSES = [
    VONQC_OT_generate_prop,
    VONQC_OT_generate_character,
    VONQC_OT_generate_npc,
    VONQC_OT_generate_viewmodel,
    VONQC_OT_generate_worldmodel,
    VONQC_OT_refresh_collections,
    VONQC_OT_collect_sequences,
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
