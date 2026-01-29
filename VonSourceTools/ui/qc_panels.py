"""
QC Generator Panels for VonSourceTools.
"""
import bpy  # type: ignore


# ============================================================================
# QC Generator Main Panel
# ============================================================================

class VON_PT_qc_generator_main(bpy.types.Panel):
    """QC Generator main panel"""
    bl_idname = "VON_PT_qc_generator_main"
    bl_label = "QC Generator"
    bl_parent_id = "VON_PT_parent"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scene = context.scene
        qc_settings = scene.von_qc_settings
        qc_type = qc_settings.enum_modelType
        should_gen_collis = qc_settings.bool_generateCollision
        layout = self.layout
        
        # Generate buttons
        row = layout.row(align=True)
        row.scale_y = 1.5
        row.operator(f"von.qcgenerator_{qc_type.lower()}", icon='CHECKMARK', text="Generate QC")
        row.operator("von.qcgenerator_preview", icon='HIDE_OFF', text="Preview")
        
        # Model settings box
        box = layout.box()
        box.label(text="Model Settings:", icon='SETTINGS')
        
        col = box.column(align=True)
        col.prop(qc_settings, "enum_modelType", text="Type")
        col.prop(qc_settings, "string_mdlModelName", text="Model Name")
        col.prop(qc_settings, "string_outputPath", text="Output Path")
        
        # Scale and collision
        col.separator()
        row = col.row(align=True)
        row.prop(qc_settings, "int_scale", text="Scale")
        
        col.prop(qc_settings, "bool_generateCollision", text="Auto-Generate Collision")
        
        if not should_gen_collis:
            col.prop(qc_settings, "string_existingCollisionCollection", text="Collision Collection")
        
        # Surface prop box
        box = layout.box()
        box.label(text="Surface Property:", icon='MATERIAL')
        col = box.column(align=True)
        col.prop(qc_settings, "enum_surfaceprop_category", text="Category")
        col.prop(qc_settings, "enum_surfaceprop_item", text="Surface")


# ============================================================================
# QC Bodygroups Panel
# ============================================================================

class VON_PT_qc_bodygroups(bpy.types.Panel):
    """QC Generator bodygroups panel"""
    bl_idname = "VON_PT_qc_bodygroups"
    bl_label = "Bodygroups"
    bl_parent_id = "VON_PT_qc_generator_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scene = context.scene
        qc_data = scene.von_qc_data
        layout = self.layout
        
        # Refresh and count controls
        row = layout.row(align=True)
        row.operator("von.qcgenerator_refresh_collections", icon='FILE_REFRESH')
        row.prop(qc_data, "num_boxes", text="Count")
        
        # Draw each bodygroup box
        for i, bodygroup_box in enumerate(qc_data.bodygroup_boxes):
            box = layout.box()
            
            # Bodygroup header
            row = box.row()
            row.prop(bodygroup_box, "name", text="", icon='GROUP')
            
            # Collection checkboxes
            col = box.column(align=True)
            for col_item in bodygroup_box.collections:
                row = col.row()
                row.prop(col_item, "enabled", text=col_item.name)


# ============================================================================
# QC Materials Panel
# ============================================================================

class VON_PT_qc_materials(bpy.types.Panel):
    """QC Generator materials panel"""
    bl_idname = "VON_PT_qc_materials"
    bl_label = "Material Paths (cdmaterials)"
    bl_parent_id = "VON_PT_qc_generator_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scene = context.scene
        qc_data = scene.von_qc_data
        layout = self.layout
        
        row = layout.row()
        row.prop(qc_data, "num_vmt_files", text="Number of Paths")
        
        col = layout.column(align=True)
        for i, vmt_item in enumerate(qc_data.vmt_filepaths):
            row = col.row(align=True)
            row.label(text=f"{i + 1}:")
            row.prop(vmt_item, "filepath", text="")


# ============================================================================
# QC Animations Panel
# ============================================================================

class VON_PT_qc_animations(bpy.types.Panel):
    """QC Generator animations panel"""
    bl_idname = "VON_PT_qc_animations"
    bl_label = "Animations"
    bl_parent_id = "VON_PT_qc_generator_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scene = context.scene
        qc_settings = scene.von_qc_settings
        qc_data = scene.von_qc_data
        layout = self.layout
        
        # Collect sequences button
        layout.operator("von.collect_sequences", icon='ACTION', text="Collect from Selected Armatures")
        
        # Character animation includes
        if qc_settings.enum_modelType in ('CHARACTER', 'NPC'):
            box = layout.box()
            box.label(text="Include Base Animations:", icon='ARMATURE_DATA')
            box.prop(qc_settings, "enum_charAnimIncludes", text="")
        
        # Display collected sequences
        if qc_data.sequence_objectdata:
            for rig_data in qc_data.sequence_objectdata:
                box = layout.box()
                box.label(text=f"Rig: {rig_data.armatureName}", icon='ARMATURE_DATA')
                
                for seq in rig_data.sequences:
                    seq_box = box.box()
                    row = seq_box.row()
                    row.prop(seq, "shouldExport", text="")
                    row.label(text=seq.originalName)
                    
                    if seq.shouldExport:
                        col = seq_box.column(align=True)
                        col.prop(seq, "sequenceName", text="Name")
                        row = col.row(align=True)
                        row.prop(seq, "enum_activity_category", text="")
                        row.prop(seq, "enum_activity", text="")
        else:
            layout.label(text="No sequences collected", icon='INFO')


# ============================================================================
# QC Advanced Panel
# ============================================================================

class VON_PT_qc_advanced(bpy.types.Panel):
    """QC Generator advanced settings panel"""
    bl_idname = "VON_PT_qc_advanced"
    bl_label = "Advanced Settings"
    bl_parent_id = "VON_PT_qc_generator_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        from ..data.paths import get_studiomdl_path
        
        scene = context.scene
        qc_settings = scene.von_qc_settings
        layout = self.layout
        
        # Definebones settings
        box = layout.box()
        box.label(text="Definebones:", icon='BONE_DATA')
        box.prop(qc_settings, "bool_shouldDefineBones", text="Generate definebones.qci")
        
        if qc_settings.bool_shouldDefineBones:
            box.operator("von.run_definebones_vondata", icon='ARMATURE_DATA', text="Run DefineBones")
        
        # StudioMDL settings
        box = layout.box()
        box.label(text="StudioMDL:", icon='CONSOLE')
        
        # Check if studiomdl is bundled/configured
        studiomdl_path = get_studiomdl_path()
        if studiomdl_path:
            row = box.row()
            row.label(text="✓ StudioMDL: Found", icon='CHECKMARK')
        else:
            row = box.row()
            row.label(text="StudioMDL: Not found", icon='ERROR')
            box.prop(qc_settings, "string_studiomdlFileLocation", text="Path")
            box.label(text="Place studiomdl.exe in addon's storeditems/external_software_dependancies/studiomdl/bin/ folder", icon='INFO')
        
        box.prop(qc_settings, "string_gmodExePath", text="GMod Path")
        box.prop(qc_settings, "bool_studiomdlVerbose", text="Verbose Output")


# ============================================================================
# Registration
# ============================================================================

CLASSES = [
    VON_PT_qc_generator_main,
    VON_PT_qc_bodygroups,
    VON_PT_qc_materials,
    VON_PT_qc_animations,
    VON_PT_qc_advanced,
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
