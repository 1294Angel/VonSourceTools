"""
Operators for QC file generation.
"""
import bpy  # type: ignore

from ..core.qc_builder import generate_qc_file, gather_qc_data_from_scene, QCData
from ..core.sequences import populate_sequence_data
from ..properties.toolbox_properties import sync_bodygroup_boxes


class VONQC_OT_generate_prop(bpy.types.Operator):
    """Generate QC file for a prop model"""
    bl_idname = "von.qcgenerator_prop"
    bl_label = "Generate Prop QC"
    bl_description = "Generate a QC file for a static prop model"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        """Check if operator can run."""
        toolbox = context.scene.toolBox
        return (toolbox.string_qcGen_outputPath != "" and 
                toolbox.string_qcGen_mdlModelName != "")
    
    def execute(self, context):
        try:
            output_path = generate_qc_file(context)
            self.report({'INFO'}, f"QC file generated: {output_path}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to generate QC: {str(e)}")
            return {'CANCELLED'}


class VONQC_OT_generate_character(bpy.types.Operator):
    """Generate QC file for a character model"""
    bl_idname = "von.qcgenerator_character"
    bl_label = "Generate Character QC"
    bl_description = "Generate a QC file for a character/player model"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        """Check if operator can run."""
        toolbox = context.scene.toolBox
        return (toolbox.string_qcGen_outputPath != "" and 
                toolbox.string_qcGen_mdlModelName != "")
    
    def execute(self, context):
        try:
            output_path = generate_qc_file(context)
            self.report({'INFO'}, f"QC file generated: {output_path}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to generate QC: {str(e)}")
            return {'CANCELLED'}


class VONQC_OT_generate_npc(bpy.types.Operator):
    """Generate QC file for an NPC model"""
    bl_idname = "von.qcgenerator_npc"
    bl_label = "Generate NPC QC"
    bl_description = "Generate a QC file for an NPC model"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        """Check if operator can run."""
        toolbox = context.scene.toolBox
        return (toolbox.string_qcGen_outputPath != "" and 
                toolbox.string_qcGen_mdlModelName != "")
    
    def execute(self, context):
        try:
            output_path = generate_qc_file(context)
            self.report({'INFO'}, f"QC file generated: {output_path}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to generate QC: {str(e)}")
            return {'CANCELLED'}


class VONQC_OT_generate_viewmodel(bpy.types.Operator):
    """Generate QC file for a viewmodel"""
    bl_idname = "von.qcgenerator_viewmodel"
    bl_label = "Generate Viewmodel QC"
    bl_description = "Generate a QC file for a first-person viewmodel"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        """Check if operator can run."""
        toolbox = context.scene.toolBox
        return (toolbox.string_qcGen_outputPath != "" and 
                toolbox.string_qcGen_mdlModelName != "")
    
    def execute(self, context):
        try:
            output_path = generate_qc_file(context)
            self.report({'INFO'}, f"QC file generated: {output_path}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to generate QC: {str(e)}")
            return {'CANCELLED'}


class VONQC_OT_generate_worldmodel(bpy.types.Operator):
    """Generate QC file for a worldmodel"""
    bl_idname = "von.qcgenerator_worldmodel"
    bl_label = "Generate Worldmodel QC"
    bl_description = "Generate a QC file for a third-person worldmodel"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        """Check if operator can run."""
        toolbox = context.scene.toolBox
        return (toolbox.string_qcGen_outputPath != "" and 
                toolbox.string_qcGen_mdlModelName != "")
    
    def execute(self, context):
        try:
            output_path = generate_qc_file(context)
            self.report({'INFO'}, f"QC file generated: {output_path}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to generate QC: {str(e)}")
            return {'CANCELLED'}


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
        from ..core.qc_builder import build_qc_content
        
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
