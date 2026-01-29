"""
Operators for Delta Animation Trick functionality.
"""
import bpy  # type: ignore

from ..core.delta_anim import (
    import_reference_armatures,
    validate_valvebiped_similarity,
    delta_anim_part_one,
    delta_anim_part_two,
    make_toe_vertical,
    clear_pose_bone_constraints,
)
from ..utils.blender_utils import select_objects


class VONANIM_OT_import_references(bpy.types.Operator):
    """Import required reference armatures for delta animation trick"""
    bl_idname = "von.deltaanimtrick_importrequiredproperties"
    bl_label = "Import Reference Armatures"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        print("----- Running Import Required Properties -----")
        try:
            has_proportions, has_male_ref, has_female_ref = import_reference_armatures()
            print(f"hasProportions={has_proportions} | hasMaleRef={has_male_ref} | hasFemaleRef={has_female_ref}")
            self.report({'INFO'}, "Reference armatures imported")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Import failed: {str(e)}")
            return {'CANCELLED'}


class VONANIM_OT_part_one(bpy.types.Operator):
    """Run part one of the delta animation trick"""
    bl_idname = "von.deltaanimtrick_partone"
    bl_label = "Delta Anim Trick (One)"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        print("----- Running Delta Anim Trick 1 -----")
        try:
            has_proportions, has_male_ref, has_female_ref = import_reference_armatures()
            
            if has_proportions and has_male_ref and has_female_ref:
                armatures = [obj for obj in bpy.data.objects if obj.type == "ARMATURE"]
                for armature in armatures:
                    delta_anim_part_one(armature)
                return {'FINISHED'}
            
            return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}


class VONANIM_OT_part_two(bpy.types.Operator):
    """Run part two of the delta animation trick"""
    bl_idname = "von.deltaanimtrick_parttwo"
    bl_label = "Delta Anim Trick (Two)"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        print("----- Running Delta Anim Trick 2 -----")
        try:
            has_proportions, has_male_ref, has_female_ref = import_reference_armatures()
            
            if has_proportions and has_male_ref and has_female_ref:
                armatures = [obj for obj in bpy.data.objects if obj.type == "ARMATURE"]
                for armature in armatures:
                    delta_anim_part_two(armature.name)
                return {'FINISHED'}
            
            return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}


class VONANIM_OT_full(bpy.types.Operator):
    """Run the complete delta animation trick process"""
    bl_idname = "von.deltaanimtrick_full"
    bl_label = "Delta Anim Trick (Full)"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        """Only enable if armatures are selected."""
        return any(obj.type == 'ARMATURE' for obj in context.selected_objects)
    
    def execute(self, context):
        print("----- Running Delta Anim Trick FULL -----")
        scene = context.scene
        delta_anim = scene.von_delta_anim
        
        failures = []
        has_valvebiped = True
        
        armatures = [obj for obj in context.selected_objects if obj.type == "ARMATURE"]
        
        if not armatures:
            self.report({'ERROR'}, "No Armature Detected")
            return {'CANCELLED'}
        
        first_obj = armatures[0]
        
        # Validate armatures
        threshold = delta_anim.float_similarityThreshold
        for armature in armatures:
            if not validate_valvebiped_similarity(armature, threshold):
                has_valvebiped = False
                failures.append(armature)
        
        if not has_valvebiped:
            for failure in failures:
                self.report(
                    {'ERROR'},
                    f"{failure.name} failed similarity threshold ({threshold}%). "
                    "Lower threshold or ensure armature uses ValveBiped bones."
                )
            return {'CANCELLED'}
        
        first_obj.select_set(True)
        
        # Import reference armatures
        try:
            has_proportions, has_male_ref, has_female_ref = import_reference_armatures()
            select_objects(armatures, armatures[0])
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
        
        if has_proportions and has_male_ref and has_female_ref:
            for armature_obj in armatures:
                bpy.context.view_layer.objects.active = armatures[0]
                
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.object.mode_set(mode='POSE')
                
                delta_anim_part_one(armature_obj)
                
                # Adjust proportions toes
                proportions_armature = bpy.data.objects["proportions"]
                bpy.context.view_layer.objects.active = proportions_armature
                bpy.ops.object.mode_set(mode='EDIT')
                
                proportions_edit_bones = proportions_armature.data.edit_bones
                for bone in proportions_edit_bones:
                    if bone.name in ["ValveBiped.Bip01_L_Toe0", "ValveBiped.Bip01_R_Toe0"]:
                        make_toe_vertical(bone)
                
                # Apply pose and clear constraints
                bpy.context.view_layer.objects.active = proportions_armature
                bpy.ops.object.mode_set(mode='POSE')
                proportions_pose_bones = proportions_armature.pose.bones
                bpy.ops.pose.armature_apply(selected=False)
                
                for bone in proportions_pose_bones:
                    clear_pose_bone_constraints(bone, proportions_armature)
                
                delta_anim_part_two(armature_obj.name)
            
            bpy.context.view_layer.objects.active = proportions_armature
            bpy.ops.object.mode_set(mode='OBJECT')
            
            self.report(
                {'INFO'},
                "Delta Anim Trick Successful | Test in HLMV and use advanced process if unsuccessful"
            )
            return {'FINISHED'}
        
        return {'CANCELLED'}


# Registration
CLASSES = [
    VONANIM_OT_import_references,
    VONANIM_OT_part_one,
    VONANIM_OT_part_two,
    VONANIM_OT_full,
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
