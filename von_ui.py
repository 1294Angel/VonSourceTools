import bpy # type: ignore
from .von_ui_operators import *

# ----------------------------
# Primary Parent Panel
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
# Parent Panels
# ----------------------------
class QC_Generator_Main(bpy.types.Panel):
    bl_idname = "VONPANEL_PT_QC_Generator_Main"
    bl_label = "QC Generator Main"
    bl_parent_id = "VONPANEL_PT_parent"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'

    def draw(self, context):
        scene = context.scene
        toolBox = scene.toolBox

        shouldGenColis = toolBox.bool_qcGen_generateCollission

        layout = self.layout
        layout.label(text="QC Generator")


        box = layout.box()
        box.label(text="Data Gathering:")

        # Split the box horizontally into two equal halves
        split = box.split(factor=0.5)
        leftCol = split.column()
        rightCol = split.column()

        # Left column
        leftCol.label(text="Main Settings:")
        leftCol.prop(toolBox, "enum_qcGen_modelType")
        leftCol.prop(toolBox, "string_qcGen_outputPath")
        leftCol.prop(toolBox, "string_qcGen_materialPath")

        # Right column
        rightCol.label(text="Advanced Options:")
        rightCol.prop(toolBox, "bool_qcGen_scale")
        rightCol.prop(toolBox, "bool_qcGen_generateCollission")
        if not shouldGenColis:
            rightCol.prop(toolBox, "string_qcGen_existingCollissionCollection")
        else: 
            rightCol.spacer
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
class VMT_Generator_Main(bpy.types.Panel):
    bl_idname = "VONPANEL_PT_VMT_Generator"
    bl_label = "VMT Generator Main"
    bl_parent_id = "VONPANEL_PT_parent"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'

    def draw(self, context):
        layout = self.layout
        layout.label(text="VMT Generator")
# ----------------------------
# Secondary Panels
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
        box = layout.box()
        box.label(text = "Step 1 - Check armature for grey bone")
        box.label(text="                Select the grey bone then the nearest green bone")
        box.label(text="                Copy constraints to selected bones")

        box.label(text = "Step 2 - Select all bones then Cntrl+A then Apply pose as rest pose")
        box.label(text = "Step 3- Change pivot to individual origins")
        box.label(text = "Step 4- Rotate toe bones until straight | Copy rotation and apply to feet bone")
        box = layout.box()
        box.operator("von.deltaanimtrick_parttwo", icon='PLAY')
        box.label(text = "Step 5 - Export your armature, proportions armature and both reference armatures")
        box.label(text = "Step 6 - Edit QC")

class QC_Generator_Advanced(bpy.types.Panel):
    bl_idname = "VONPANEL_PT_QC_Generator_Advanced"
    bl_label = "QC Generator Advanced"
    bl_parent_id = "VONPANEL_PT_QC_Generator_Main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'

    def draw(self, context):
        scene = context.scene
        toolBox = scene.toolBox

        layout = self.layout
        layout.label(text="QC Generator")

classes = (
    #Base Panel
    Parent_Panel,

    #Parent Panels
    Delta_Animations,
    QC_Generator_Main,
    VMT_Generator_Main,

    #Primary Child Panels
    Delta_Animations_Advanced,
    QC_Generator_Advanced
)


def von_ui_register():
    for cls in classes:
        bpy.utils.register_class(cls)    




def von_ui_unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)