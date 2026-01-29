"""
Delta Animation Panels for VonSourceTools.
"""
import bpy  # type: ignore


# ============================================================================
# Delta Animations Main Panel
# ============================================================================

class VON_PT_delta_animations(bpy.types.Panel):
    """Delta animations simple panel"""
    bl_idname = "VON_PT_delta_animations"
    bl_label = "Delta Animation Trick"
    bl_parent_id = "VON_PT_parent"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scene = context.scene
        toolbox = scene.toolBox
        layout = self.layout
        
        layout.label(text="Delta Animation Trick")
        layout.label(text="Creates delta animations for Source Engine")
        
        # Similarity threshold
        box = layout.box()
        box.label(text="Settings:")
        box.prop(toolbox, "float_deltaAnim_similarityThreshold", text="Similarity Threshold %")
        
        # Simple one-click operation
        box = layout.box()
        box.label(text="Quick Mode:")
        box.label(text="Select your armature and click below")
        row = box.row()
        row.scale_y = 1.5
        row.operator("von.deltaanimtrick_full", icon='ARMATURE_DATA')


# ============================================================================
# Delta Animations Advanced Panel
# ============================================================================

class VON_PT_delta_advanced(bpy.types.Panel):
    """Delta animations advanced panel"""
    bl_idname = "VON_PT_delta_advanced"
    bl_label = "Delta Animation Advanced"
    bl_parent_id = "VON_PT_delta_animations"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text="Step-by-step Mode:")
        
        # Step 1
        box = layout.box()
        box.label(text="Step 1: Import References")
        box.label(text="Imports proportions and reference armatures")
        box.operator("von.deltaanimtrick_importrefs", icon='IMPORT')
        
        # Step 2
        box = layout.box()
        box.label(text="Step 2: Part One")
        box.label(text="Sets up constraints and initial pose")
        box.operator("von.deltaanimtrick_partone", icon='CONSTRAINT')
        
        # Step 3
        box = layout.box()
        box.label(text="Step 3: Part Two")
        box.label(text="Applies transformations and cleanup")
        box.operator("von.deltaanimtrick_parttwo", icon='CHECKMARK')


# ============================================================================
# Registration
# ============================================================================

CLASSES = [
    VON_PT_delta_animations,
    VON_PT_delta_advanced,
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
