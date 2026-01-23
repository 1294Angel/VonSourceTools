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
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scene = context.scene
        toolBox = scene.toolBox
        qcType = toolBox.enum_qcGen_modelType
        shouldGenColis = toolBox.bool_qcGen_generateCollission
        layout = self.layout
        
        layout.label(text="QC Generator")
        layout.operator(f"von.qcgenerator_{qcType.lower()}")

        box = layout.box()
        box.label(text="Data Gathering:")
        split = box.split(factor=0.5)
        leftCol = split.column()
        rightCol = split.column()

        # Left column
        leftCol.label(text="Main Settings:")
        leftCol.prop(toolBox, "enum_qcGen_modelType")
        leftCol.prop(toolBox, "string_qcGen_outputPath")

        # Right column
        rightCol.label(text="Advanced Options:")
        rightCol.prop(toolBox, "int_qcGen_scale")
        rightCol.prop(toolBox, "bool_qcGen_generateCollission")
        if not shouldGenColis:
            rightCol.prop(toolBox, "string_qcGen_existingCollissionCollection")
        else: 
            rightCol.label(text="Will Generate Collission")
        
        box = layout.box()
        box.label(text="SurfaceProp:")
        box.prop(toolBox, "enum_surfaceprop_category")
        box.prop(toolBox, "enum_surfaceprop_item")
        
        
    

class Delta_Animations(bpy.types.Panel):
    bl_idname = "VONPANEL_PT_delta_animations"
    bl_label = "Delta Animation Trick Simple"
    bl_parent_id = "VONPANEL_PT_parent"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}

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
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="VMT Generator")

class Batch_SMD_Export(bpy.types.Panel):
    bl_idname = "VONPANEL_PT_SMD_EXPORT"
    bl_label = "Batch SMD Export"
    bl_parent_id = "VONPANEL_PT_parent"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scene = context.scene
        toolBox = scene.toolBox
        layout = self.layout
        layout.label(text="Collections:")
        layout.operator(OBJECT_OT_split_objects.bl_idname, icon='OUTLINER_OB_GROUP_INSTANCE')
        layout.operator(OBJECT_OT_restore_objects.bl_idname, icon='FILE_REFRESH')

        layout.separator()
        layout.label(text="Export:")
        layout.prop(toolBox, "export_folder", text="Folder")
        layout.operator(OBJECT_OT_export_smd.bl_idname, icon='EXPORT')    
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
    bl_options = {'DEFAULT_CLOSED'}

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

class QC_Generator_Bodygroups(bpy.types.Panel):
    bl_idname = "VONPANEL_PT_QC_Generator_Bodygroups"
    bl_label = "QC Generator Bodygroups"
    bl_parent_id = "VONPANEL_PT_QC_Generator_Main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scene = context.scene
        toolBox = scene.toolBox
        qcData = scene.QC_PrimaryData
        layout = self.layout
        layout.label(text="Bodygroup Definer")

        box = layout.box()
        box.operator("von.qcgenerator_refresh_collections", icon='FILE_REFRESH')
        box = layout.box()
        box.label(text="Bodygroups:")
        box.prop(qcData, "num_boxes")
        for bg_box in qcData.bodygroup_boxes:
            bg_ui = box.box()
            bg_ui.prop(bg_box, "name", text="Bodygroup")

            for item in bg_box.collections:
                bg_ui.prop(item, "enabled", text=item.name)

class QC_Generator_MaterialFolders(bpy.types.Panel):
    bl_idname = "VONPANEL_PT_QC_Generator_MaterialFolders"
    bl_label = "QC Generator MaterialFolders"
    bl_parent_id = "VONPANEL_PT_QC_Generator_Main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}
   

    def draw(self, context):
        scene = context.scene
        toolBox = scene.toolBox
        qcData = scene.QC_PrimaryData
        layout = self.layout
        layout.label(text="Bodygroup Material Folder Locations")

        box = layout.box()
        box.label(text="VMT Filepaths:")
        box.prop(qcData, "num_vmt_files")

        for i, vmt_item in enumerate(qcData.vmt_filepaths):
            box.prop(vmt_item, "filepath", text=f"VMT {i+1}")

class QC_Generator_AnimSel(bpy.types.Panel):
    bl_idname = "VONPANEL_PT_QC_Anim_Sel"
    bl_label = "QC Generator Animation Selector"
    bl_parent_id = "VONPANEL_PT_QC_Generator_Main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        primaryData = context.scene.QC_PrimaryData

        layout.operator("von.collect_sequences", icon='ARMATURE_DATA')

        for rig in primaryData.sequence_objectdata:
            box = layout.box()
            box.label(text=rig.armatureName, icon='ARMATURE_DATA')

            for seq in rig.sequences:
                row = box.row()
                row.prop(seq, "shouldExport", text="")
                row.label(text=seq.sequenceName)


class QC_Generator_Advanced(bpy.types.Panel):
    bl_idname = "VONPANEL_PT_QC_Generator_Advanced"
    bl_label = "QC Generator Advanced"
    bl_parent_id = "VONPANEL_PT_QC_Generator_Main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scene = context.scene
        toolBox = scene.toolBox

        layout = self.layout
        layout.label(text="QC Generator Advanced Settings")

# ----------------------------
# Tertiary Panels
# ----------------------------
class QC_Generator_AttachmentPointBones(bpy.types.Panel):
    bl_idname = "VONPANEL_PT_QC_Attach_Point"
    bl_label = "QC Generator Attachment Point Definer"
    bl_parent_id = "VONPANEL_PT_QC_Generator_Advanced"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scene = context.scene
        toolBox = scene.toolBox
        qcData = scene.QC_PrimaryData
        layout = self.layout
        layout.label(text="Attachment Point Definer")


classes = (
    #Base Panel
    Parent_Panel,

    #Primary Parent Panels
    Delta_Animations,
    QC_Generator_Main,
    VMT_Generator_Main,
    Batch_SMD_Export,

    #Primary Child Panels
    Delta_Animations_Advanced,
    QC_Generator_MaterialFolders,
    QC_Generator_AnimSel,
    QC_Generator_Bodygroups,
    QC_Generator_Advanced,

    #Secondary Child Panels
    QC_Generator_AttachmentPointBones
)


def von_ui_register():
    for cls in classes:
        bpy.utils.register_class(cls)    




def von_ui_unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)