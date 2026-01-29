"""
VMT Generator / Material to VTF Panels for VonSourceTools.
"""
import bpy  # type: ignore


# ============================================================================
# Material List UI
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


# ============================================================================
# VMT Generator Main Panel
# ============================================================================

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
        
        # VTFCmd path with status indicator
        from ..data.paths import get_vtfcmd_path
        bundled_vtfcmd = get_vtfcmd_path()
        
        if bundled_vtfcmd is not None:
            row = col.row()
            row.label(text="VTFCmd:", icon='CHECKMARK')
            row.label(text="Found (bundled)")
        else:
            col.label(text="VTFCmd Path (not bundled):")
            col.prop(scene.von_vtfcmd_path, "path", text="")
            if not scene.von_vtfcmd_path.path:
                col.label(text="Place VTFCmd.exe in addon's tools/vtfcmd/ folder", icon='INFO')
        
        col.separator()
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


# ============================================================================
# VMT Material Settings Panel
# ============================================================================

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
# Registration
# ============================================================================

CLASSES = [
    VON_UL_MaterialList,
    VON_PT_vmt_generator,
    VON_PT_vmt_material_settings,
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
