"""
UI Panels for QC Functionality
"""
import bpy  # type: ignore

# ============================================================================
# QC Generator Panels
# ============================================================================

class VON_PT_qc_generator_main(bpy.types.Panel):
    """QC Generator main panel"""
    bl_idname = "VON_PT_qc_generator_main"
    bl_label = "QC Generator Main"
    bl_parent_id = "VON_PT_parent"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scene = context.scene
        toolbox = scene.toolBox
        qc_type = toolbox.enum_qcGen_modelType
        should_gen_collis = toolbox.bool_qcGen_generateCollission
        layout = self.layout
        
        layout.label(text="QC Generator")
        
        # Generate button
        row = layout.row()
        row.scale_y = 2
        row.operator(f"von.qcgenerator_{qc_type.lower()}", icon='CHECKMARK')
        
        # Data gathering box
        box = layout.box()
        box.label(text="Data Gathering:")
        split = box.split(factor=0.5)
        
        # Left column - Main settings
        left_col = split.column()
        left_col.label(text="Main Settings:")
        left_col.prop(toolbox, "enum_qcGen_modelType")
        left_col.prop(toolbox, "string_qcGen_outputPath")
        
        # Right column - Advanced options
        right_col = split.column()
        right_col.label(text="Advanced Options:")
        right_col.prop(toolbox, "int_qcGen_scale")
        right_col.prop(toolbox, "bool_qcGen_generateCollission")
        
        if not should_gen_collis:
            right_col.prop(toolbox, "string_qcGen_existingCollissionCollection")
        else:
            right_col.label(text="Will Generate Collision")
        
        # Surface prop box
        box = layout.box()
        box.label(text="SurfaceProp:")
        box.prop(toolbox, "enum_surfaceprop_category")
        box.prop(toolbox, "enum_surfaceprop_item")


class VON_PT_qc_bodygroups(bpy.types.Panel):
    """QC Generator bodygroups panel"""
    bl_idname = "VON_PT_qc_bodygroups"
    bl_label = "QC Generator Bodygroups"
    bl_parent_id = "VON_PT_qc_generator_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scene = context.scene
        qc_data = scene.QC_PrimaryData
        layout = self.layout
        
        layout.label(text="Bodygroup Definer")
        
        box = layout.box()
        box.operator("von.qcgenerator_refresh_collections", icon='FILE_REFRESH')
        
        box = layout.box()
        box.label(text="Bodygroups:")
        box.prop(qc_data, "num_boxes")
        
        for bg_box in qc_data.bodygroup_boxes:
            bg_ui = box.box()
            bg_ui.prop(bg_box, "name", text="Bodygroup")
            
            for item in bg_box.collections:
                bg_ui.prop(item, "enabled", text=item.name)


class VON_PT_qc_materials(bpy.types.Panel):
    """QC Generator material folders panel"""
    bl_idname = "VON_PT_qc_materials"
    bl_label = "QC Generator MaterialFolders"
    bl_parent_id = "VON_PT_qc_generator_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scene = context.scene
        qc_data = scene.QC_PrimaryData
        layout = self.layout
        
        layout.label(text="Bodygroup Material Folder Locations")
        
        box = layout.box()
        box.label(text="VMT Filepaths:")
        box.prop(qc_data, "num_vmt_files")
        
        for i, vmt_item in enumerate(qc_data.vmt_filepaths):
            box.prop(vmt_item, "filepath", text=f"VMT {i+1}")


class VON_PT_qc_animations(bpy.types.Panel):
    """QC Generator animation selector panel"""
    bl_idname = "VON_PT_qc_animations"
    bl_label = "QC Generator Animation Selector"
    bl_parent_id = "VON_PT_qc_generator_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        primary_data = context.scene.QC_PrimaryData
        
        layout.operator("von.collect_sequences", icon='ARMATURE_DATA')
        
        for rig in primary_data.sequence_objectdata:
            rig_box = layout.box()
            rig_box.label(text=rig.armatureName, icon='ARMATURE_DATA')
            
            for seq in rig.sequences:
                seq_box = rig_box.box()
                seq_box.label(text=f"AnimFile = {seq.originalName}")
                row = seq_box.row()
                row.prop(seq, "shouldExport", text="")
                row.prop(seq, "sequenceName", text="")
                seq_box.prop(seq, "enum_activity_category")
                seq_box.prop(seq, "enum_activity")


class VON_PT_qc_advanced(bpy.types.Panel):
    """QC Generator advanced settings panel"""
    bl_idname = "VON_PT_qc_advanced"
    bl_label = "QC Generator Advanced"
    bl_parent_id = "VON_PT_qc_generator_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="QC Generator Advanced Settings")

# ============================================================================
# Registration
# ============================================================================

CLASSES = [
    
    # QC Generator panels
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
