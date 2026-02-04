import bpy

# ============================================================================
# Texture Atlas Panel
# ============================================================================

class VON_PT_texture_atlas(bpy.types.Panel):
    bl_label = "Texture Atlas"
    bl_idname = "VON_PT_texture_atlas"
    bl_parent_id = "VON_PT_parent"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        atlasSettings = context.scene.von_textureatlas_settings
        layout = self.layout
        layout.label(text= "Texture Atlasing Toolset!")
        row = layout.row()
        row.prop(atlasSettings, "atlas_size")
        row = layout.row()
        row.prop(atlasSettings, "atlas_moveUVs")
        if atlasSettings.atlas_moveUVs:
            row.prop(atlasSettings, "atlas_applymaterial") 
        row = layout.row()
        row.prop(atlasSettings, "atlas_materialname")
        row = layout.row()
        row.prop(atlasSettings, "atlas_output_path")
        
        layout = self.layout
        layout.operator("von.optimisationtools_textureatlasing", text="Texture Atlas")
        
# ============================================================================
# Register
# ============================================================================

CLASSES = [
    VON_PT_texture_atlas
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)