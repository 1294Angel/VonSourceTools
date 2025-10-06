import bpy # type: ignore
from .von_ui_operators import *

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Menu Layout

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



# ----------------------------
# Parent Panel
# ----------------------------
class Parent_Panel(bpy.types.Panel):
    bl_idname = "VONPANEL_PT_parent"
    bl_label = "Von Source Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self,context):
        layout = self.layout

# ----------------------------
# Child Panel: Delta Animations
# ----------------------------

class Delta_Animations(bpy.types.Panel):
    bl_idname = "VONPANEL_PT_delta_animations"
    bl_label = "Delta Animation Trick Simple"
    bl_parent_id = "VONPANEL_PT_parent"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'

    def draw(self, context):
        layout = self.layout
        layout.label(text="Delta Animation Trick")
        layout.operator("von.deltaanimtrick_full", icon='PLAY')

# ----------------------------
# Child Panel: Delta Animations Advanced
# ----------------------------
class Delta_Animations_Advanced(bpy.types.Panel):
    bl_idname = "VONPANEL_PT_delta_animations_advanced"
    bl_label = "Delta Anim Trick Advanced Settings"
    bl_parent_id = "VONPANEL_PT_delta_animations"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'

    def draw(self, context):
        scene = context.scene
        toolBox = scene.toolBox

        layout = self.layout
        layout.label(text="Delta Animation Trick Advanced")

        box = layout.box()
        box.label(text = "Settings -")
        box.prop(toolBox, "float_deltaAnim_simmilarityThreshold")

        box = layout.box()
        box.label(text = "Functions -")
        box.operator("von.deltaanimtrick_importrequiredproperties")
        box.operator("von.deltaanimtrick_partone", icon='PLAY')
        box.operator("von.deltaanimtrick_parttwo", icon='PLAY')





classes = (
    #Menu UI
    Parent_Panel,
    Delta_Animations,
    Delta_Animations_Advanced
)


def von_ui_register():
    for cls in classes:
        bpy.utils.register_class(cls)    




def von_ui_unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)