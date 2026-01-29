"""
UI Panels for VonSourceTools.
"""
import bpy  # type: ignore


# ============================================================================
# Parent Panel
# ============================================================================

class VON_PT_parent(bpy.types.Panel):
    """Main parent panel for VonSourceTools"""
    bl_idname = "VON_PT_parent"
    bl_label = "Von Source Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw(self, context):
        layout = self.layout


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
# Delta Animation Panels
# ============================================================================

class VON_PT_delta_animations(bpy.types.Panel):
    """Delta Animation Trick panel"""
    bl_idname = "VON_PT_delta_animations"
    bl_label = "Delta Animation Trick Simple"
    bl_parent_id = "VON_PT_parent"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Delta Animation Trick")
        layout.operator("von.deltaanimtrick_full", icon='PLAY')


class VON_PT_delta_advanced(bpy.types.Panel):
    """Delta Animation Trick advanced settings panel"""
    bl_idname = "VON_PT_delta_advanced"
    bl_label = "Delta Anim Trick Advanced Settings"
    bl_parent_id = "VON_PT_delta_animations"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scene = context.scene
        toolbox = scene.toolBox
        layout = self.layout
        
        layout.label(text="Delta Animation Trick Advanced")
        
        # Settings
        box = layout.box()
        box.label(text="Settings -")
        box.prop(toolbox, "float_deltaAnim_similarityThreshold")
        
        # Functions
        box = layout.box()
        box.label(text="Functions -")
        box.operator("von.deltaanimtrick_importrequiredproperties")
        box.operator("von.deltaanimtrick_partone", icon='PLAY')
        
        # Instructions
        box = layout.box()
        box.label(text="Step 1 - Check armature for grey bone")
        box.label(text="        Select the grey bone then nearest green bone")
        box.label(text="        Copy constraints to selected bones")
        box.label(text="Step 2 - Select all bones then Ctrl+A then Apply pose as rest pose")
        box.label(text="Step 3 - Change pivot to individual origins")
        box.label(text="Step 4 - Rotate toe bones until straight | Copy rotation and apply to feet bone")
        
        box = layout.box()
        box.operator("von.deltaanimtrick_parttwo", icon='PLAY')
        box.label(text="Step 5 - Export your armature, proportions armature and both reference armatures")
        box.label(text="Step 6 - Edit QC")


# ============================================================================
# VMT Generator / Material to VTF Panels
# ============================================================================

class VON_UL_MaterialList(bpy.types.UIList):
    """UI List for displaying materials with checkboxes."""
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        """Draw each item in the UI list."""
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            split = layout.split(factor=0.1, align=True)
            split.prop(item, "material_checkbox", text="")
            split.label(text=item.material_name, icon='MATERIAL')
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='MATERIAL')


class VON_PT_vmt_generator(bpy.types.Panel):
    """Material to VTF/VMT Generator main panel"""
    bl_idname = "VON_PT_vmt_generator"
    bl_label = "Material to VTF Converter"
    bl_parent_id = "VON_PT_parent"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Materials section
        box = layout.box()
        box.label(text="Materials Selection:", icon='MATERIAL_DATA')
        
        # Materials list
        row = box.row()
        row.template_list(
            "VON_UL_MaterialList", "",
            scene, "von_mats_collection",
            scene, "von_mats_index",
            rows=4
        )
        
        # Material list controls
        row = box.row(align=True)
        row.operator("von.vtf_refresh_materials", icon='FILE_REFRESH', text="Refresh")
        row.operator("von.vtf_select_all", text="All")
        row.operator("von.vtf_deselect_all", text="None")
        
        # Paths section
        box = layout.box()
        box.label(text="Paths Configuration:", icon='FILEBROWSER')
        
        col = box.column(align=True)
        col.label(text="VTFCmd Path:")
        col.prop(scene.von_vtfcmd_path, "path", text="")
        
        col.label(text="Material Output Path:")
        col.prop(scene.von_material_output_path, "path", text="")
        
        # VTF Parameters section
        box = layout.box()
        box.label(text="VTF Parameters:", icon='SETTINGS')
        
        col = box.column(align=True)
        
        # Format settings
        row = col.row(align=True)
        row.prop(scene, "von_vtf_format", text="Format")
        row.prop(scene, "von_vtf_alpha_format", text="Alpha")
        
        col.prop(scene, "von_vtf_version", text="Version")
        
        # Resize settings
        col.separator()
        col.prop(scene, "von_vtf_resize_bool", text="Enable Resize")
        
        if scene.von_vtf_resize_bool:
            resize_box = col.box()
            resize_col = resize_box.column(align=True)
            resize_col.prop(scene, "von_vtf_resize_method", text="Method")
            resize_col.prop(scene, "von_vtf_resize_filter", text="Filter")
            resize_col.prop(scene, "von_vtf_clamp_size", text="Clamp Size")
        
        # VMT settings
        col.separator()
        col.prop(scene, "von_vmt_generate_bool", text="Generate VMT Files")
        
        if scene.von_vmt_generate_bool:
            vmt_box = col.box()
            vmt_col = vmt_box.column(align=True)
            vmt_col.prop(scene, "von_vmt_shader", text="Shader")
            
            vmt_col.separator()
            vmt_col.label(text="Global VMT Parameters:")
            param_row = vmt_col.row(align=True)
            param_row.prop(scene, "von_vmt_param_additive", text="Additive")
            param_row.prop(scene, "von_vmt_param_translucent", text="Translucent")
            vmt_col.prop(scene, "von_vmt_param_nocull", text="No Cull")
        
        # Convert button
        layout.separator()
        convert_row = layout.row()
        convert_row.scale_y = 1.5
        convert_row.operator("von.vtf_convert_materials", icon='EXPORT')


class VON_PT_vmt_material_settings(bpy.types.Panel):
    """Per-material VMT settings panel"""
    bl_idname = "VON_PT_vmt_material_settings"
    bl_label = "VMT Material Settings"
    bl_parent_id = "VON_PT_vmt_generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        """Only show when VMT generation is enabled and materials exist."""
        scene = context.scene
        return (hasattr(scene, 'von_vmt_generate_bool') and 
                scene.von_vmt_generate_bool and 
                len(scene.von_mats_collection) > 0)
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Get selected material for VMT editing
        if 0 <= scene.von_mats_index < len(scene.von_mats_collection):
            selected_mat = scene.von_mats_collection[scene.von_mats_index]
            vmt_params = selected_mat.vmt_params
            
            # Material selection info
            info_row = layout.row()
            info_row.label(text=f"Editing: {selected_mat.material_name}", icon='MATERIAL_DATA')
            
            # Texture Maps section
            maps_box = layout.box()
            maps_box.label(text="Texture Maps:", icon='TEXTURE')
            maps_col = maps_box.column(align=True)
            
            maps_col.prop(vmt_params, "normal_map", text="Normal Map")
            maps_col.prop(vmt_params, "phong_exponent_map", text="Phong Exponent Map")
            
            # Phong Shading section
            phong_box = layout.box()
            phong_box.label(text="Phong Shading:", icon='SHADING_RENDERED')
            phong_col = phong_box.column(align=True)
            
            phong_col.prop(vmt_params, "enable_phong")
            if vmt_params.enable_phong:
                phong_sub = phong_col.box()
                phong_sub_col = phong_sub.column(align=True)
                phong_sub_col.prop(vmt_params, "phong_boost")
                phong_sub_col.prop(vmt_params, "phong_albedo_tint")
                phong_sub_col.prop(vmt_params, "phong_albedo_boost")
                phong_sub_col.prop(vmt_params, "phong_fresnel_ranges")
            
            # Rim Lighting section
            rim_box = layout.box()
            rim_box.label(text="Rim Lighting:", icon='LIGHT_SUN')
            rim_col = rim_box.column(align=True)
            
            rim_col.prop(vmt_params, "enable_rimlight")
            if vmt_params.enable_rimlight:
                rim_sub = rim_col.box()
                rim_sub_col = rim_sub.column(align=True)
                rim_sub_col.prop(vmt_params, "rimlight_exponent")
                rim_sub_col.prop(vmt_params, "rimlight_boost")
                rim_sub_col.prop(vmt_params, "rim_mask")
            
            # Environment Mapping section
            env_box = layout.box()
            env_box.label(text="Environment Mapping:", icon='WORLD')
            env_col = env_box.column(align=True)
            
            env_col.prop(vmt_params, "enable_envmap")
            if vmt_params.enable_envmap:
                env_sub = env_col.box()
                env_sub_col = env_sub.column(align=True)
                env_sub_col.prop(vmt_params, "envmap_tint")
                env_sub_col.prop(vmt_params, "normal_map_alpha_envmap_mask")
            
            # Advanced Parameters section
            adv_box = layout.box()
            adv_box.label(text="Advanced Parameters:", icon='PREFERENCES')
            adv_col = adv_box.column(align=True)
            
            adv_col.prop(vmt_params, "color2")
            adv_col.prop(vmt_params, "blend_tint_by_base_alpha")
        else:
            layout.label(text="No material selected", icon='INFO')


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
        layout = self.layout
        scene = context.scene
        toolbox = scene.toolBox
        
        layout.label(text="Image Filetype Converter")
        layout.label(text="Blender might hang if converting to or from vtf")
        layout.label(text="May take a few minutes")
        
        row = layout.row()
        row.prop(toolbox, "string_vtfbatch_inputfolder", text="Input Folder")
        row.prop(toolbox, "string_vtfbatch_outputfolder", text="Output Folder")
        
        row = layout.row()
        row.prop(toolbox, "enum_vtfbatch_sourcefiletype", text="Source Filetype")
        row.prop(toolbox, "enum_vtfbatch_targetfiletype", text="Target Filetype")
        
        layout.operator("von.batchconvertfiletypes", text="Run Conversion")


# ============================================================================
# SMD Export Panel
# ============================================================================

class VON_PT_smd_export(bpy.types.Panel):
    """Batch SMD export panel"""
    bl_idname = "VON_PT_smd_export"
    bl_label = "Batch SMD Export"
    bl_parent_id = "VON_PT_parent"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scene = context.scene
        toolbox = scene.toolBox
        layout = self.layout
        
        layout.label(text="Collections:")
        layout.operator("object.split_objects", icon='OUTLINER_OB_GROUP_INSTANCE')
        layout.operator("object.restore_objects", icon='FILE_REFRESH')
        
        layout.separator()
        
        layout.label(text="Export:")
        layout.prop(toolbox, "string_export_folder", text="Folder")
        layout.operator("object.export_smd", icon='EXPORT')


# ============================================================================
# Registration
# ============================================================================

CLASSES = [
    # Parent panel
    VON_PT_parent,
    
    # QC Generator panels
    VON_PT_qc_generator_main,
    VON_PT_qc_bodygroups,
    VON_PT_qc_materials,
    VON_PT_qc_animations,
    VON_PT_qc_advanced,
    
    # Delta animation panels
    VON_PT_delta_animations,
    VON_PT_delta_advanced,
    
    # Material to VTF / VMT Generator
    VON_UL_MaterialList,
    VON_PT_vmt_generator,
    VON_PT_vmt_material_settings,
    
    # Other panels
    VON_PT_image_converter,
    VON_PT_smd_export,
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
