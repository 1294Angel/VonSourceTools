"""
Operators for Material to VTF conversion.

These operators handle:
- Refreshing the materials list from scene objects
- Converting materials to VTF format (threaded)
- Generating VMT files
"""
import bpy
import os
from bpy.types import Operator

from ..core.material_vtf import (
    get_image_texture_node,
    validate_image_texture,
    get_materials_relative_path,
    process_additional_textures,
    generate_vmt_content,
    write_vmt_file,
    build_vtfcmd_command,
    execute_vtfcmd,
    collect_scene_materials,
)
from ..utils.threading_utils import (
    run_in_background,
    get_task_result,
    is_task_finished,
    cleanup_task,
    TaskStatus,
)


class VONVTF_OT_refresh_materials(Operator):
    """Refresh the materials list from scene objects."""
    bl_idname = "von.vtf_refresh_materials"
    bl_label = "Refresh Materials List"
    bl_description = "Refresh the list of materials from all objects in the scene"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        """Check if the operator can run."""
        return len(bpy.data.materials) > 0

    def execute(self, context):
        """Execute the operator."""
        scene = context.scene
        
        # Clear collection first
        scene.von_mats_collection.clear()
        
        # Collect materials from scene
        material_slots = collect_scene_materials(context)
        
        if material_slots:
            for material_slot in material_slots:
                item = scene.von_mats_collection.add()
                item.material_checkbox = True
                item.material_name = material_slot.material.name
                item.material = material_slot.material
            
            self.report({'INFO'}, f"Found {len(scene.von_mats_collection)} materials")
        else:
            self.report({'WARNING'}, "No materials found in scene")
            
        return {'FINISHED'}


def _vtf_conversion_task(
    vtfcmd_exe,
    image_paths,
    image_name_mapping,
    output_path,
    vtf_format,
    alpha_format,
    vtf_version,
    resize,
    resize_method,
    resize_filter,
    clamp_size,
    shader,
    vmt_params,
    additional_texture_paths
):
    """
    Background task function for VTF conversion.
    
    This runs in a separate thread to avoid blocking Blender.
    """
    command_line = build_vtfcmd_command(
        vtfcmd_exe=vtfcmd_exe,
        image_paths=image_paths,
        image_name_mapping=image_name_mapping,
        output_path=output_path,
        vtf_format=vtf_format,
        alpha_format=alpha_format,
        vtf_version=vtf_version,
        resize=resize,
        resize_method=resize_method,
        resize_filter=resize_filter,
        clamp_size=clamp_size,
        shader=shader,
        vmt_params=vmt_params,
        additional_texture_paths=additional_texture_paths
    )
    
    # Print command for debugging
    command_str = ' '.join(f'"{arg}"' if ' ' in arg else arg for arg in command_line)
    print(f"Executing VTFCmd: {command_str}")
    
    success, stdout, stderr = execute_vtfcmd(command_line)
    
    return {
        'success': success,
        'stdout': stdout,
        'stderr': stderr,
        'num_files': len(image_paths),
        'command': command_str,
    }


class VONVTF_OT_convert_materials(Operator):
    """Convert selected materials to VTF format (threaded)."""
    bl_idname = "von.vtf_convert_materials"
    bl_label = "Convert to VTF"
    bl_description = "Convert selected materials to VTF format using VTFCmd"
    bl_options = {'REGISTER'}
    
    # Modal state
    _timer = None
    _task_id = None
    _material_objects = None
    _all_additional_textures = None

    @classmethod
    def poll(cls, context):
        """Check if the operator can run."""
        from ..data.paths import get_vtfcmd_path
        
        scene = context.scene
        
        # Check if output path is set
        if not (hasattr(scene, 'von_material_output_path') and 
                scene.von_material_output_path and 
                scene.von_material_output_path.path != ""):
            return False
        
        # Check if VTFCmd is available (bundled or UI path)
        bundled_vtfcmd = get_vtfcmd_path()
        if bundled_vtfcmd is not None:
            return True
        
        # Fall back to UI path
        return (hasattr(scene, 'von_vtfcmd_path') and 
                scene.von_vtfcmd_path and 
                scene.von_vtfcmd_path.path != "")

    def execute(self, context):
        """Start the conversion process."""
        scene = context.scene
        
        image_paths = []
        image_name_mapping = {}
        material_objects = []
        all_additional_textures = {}
        
        # Process each selected material
        for mat_object in scene.von_mats_collection:
            if not mat_object.material_checkbox:
                continue
                
            material = mat_object.material
            if not material:
                continue
                
            # Get image texture node
            image_node = get_image_texture_node(material)
            if not image_node:
                self.report({'ERROR'}, f"Material '{material.name}' has no Image Texture node connected to Base Color")
                return {'CANCELLED'}
            
            # Validate image
            image_path, error_msg = validate_image_texture(image_node)
            if error_msg:
                self.report({'ERROR'}, f"Material '{material.name}': {error_msg}")
                return {'CANCELLED'}
            
            image_paths.append(image_path)
            image_name_mapping[image_path] = mat_object.material_name
            material_objects.append(mat_object)
            
            # Process additional textures for this material
            if scene.von_vmt_generate_bool:
                additional_textures = process_additional_textures(
                    mat_object.material_name,
                    mat_object.vmt_params,
                    scene.von_material_output_path.path
                )
                if additional_textures:
                    all_additional_textures[mat_object.material_name] = additional_textures
        
        if not image_paths:
            self.report({'ERROR'}, "No valid materials selected for conversion")
            return {'CANCELLED'}
        
        # Store for later VMT generation
        self._material_objects = material_objects
        self._all_additional_textures = all_additional_textures
        
        # Collect all additional texture paths for VTFCmd
        additional_texture_paths = {}
        for mat_name, tex_dict in all_additional_textures.items():
            for tex_type, tex_path in tex_dict.items():
                if tex_type not in additional_texture_paths:
                    additional_texture_paths[tex_type] = []
                additional_texture_paths[tex_type].append(tex_path)
        
        # Build VTFCmd path - check bundled version first, then UI path
        from ..data.paths import get_vtfcmd_path
        
        bundled_vtfcmd = get_vtfcmd_path()
        if bundled_vtfcmd is not None:
            vtfcmd_exe = str(bundled_vtfcmd)
        else:
            # Fall back to UI-specified path
            vtfcmd_path = scene.von_vtfcmd_path.path
            if not vtfcmd_path:
                self.report({'ERROR'}, "VTFCmd path not set. Either place VTFCmd in the addon's tools/vtfcmd folder or specify the path in the UI.")
                return {'CANCELLED'}
            if not vtfcmd_path.endswith(os.sep):
                vtfcmd_path += os.sep
            vtfcmd_exe = os.path.join(vtfcmd_path, "VTFCmd.exe")
        
        # Get VMT parameters if enabled
        vmt_params = None
        shader = None
        if scene.von_vmt_generate_bool:
            shader = scene.von_vmt_shader
            vmt_params = {
                'additive': scene.von_vmt_param_additive,
                'translucent': scene.von_vmt_param_translucent,
                'nocull': scene.von_vmt_param_nocull,
            }
        
        # Start background task
        self._task_id = run_in_background(
            _vtf_conversion_task,
            vtfcmd_exe,
            image_paths,
            image_name_mapping,
            scene.von_material_output_path.path,
            scene.von_vtf_format,
            scene.von_vtf_alpha_format,
            scene.von_vtf_version,
            scene.von_vtf_resize_bool,
            scene.von_vtf_resize_method,
            scene.von_vtf_resize_filter,
            scene.von_vtf_clamp_size,
            shader,
            vmt_params,
            additional_texture_paths
        )
        
        # Set up modal timer
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        
        self.report({'INFO'}, "VTF conversion started in background...")
        return {'RUNNING_MODAL'}
    
    def modal(self, context, event):
        """Check task completion."""
        if event.type == 'TIMER':
            if is_task_finished(self._task_id):
                return self._finish(context)
        
        return {'PASS_THROUGH'}
    
    def _finish(self, context):
        """Handle task completion."""
        # Remove timer
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        
        # Get result
        result = get_task_result(self._task_id)
        cleanup_task(self._task_id)
        
        if result is None:
            self.report({'ERROR'}, "Task result not found")
            return {'CANCELLED'}
        
        if result.status == TaskStatus.FAILED:
            self.report({'ERROR'}, f"VTF conversion failed: {result.error}")
            return {'CANCELLED'}
        
        if result.status == TaskStatus.CANCELLED:
            self.report({'WARNING'}, "VTF conversion was cancelled")
            return {'CANCELLED'}
        
        # Process successful result
        task_result = result.result
        if task_result['success']:
            self.report({'INFO'}, f"Successfully processed {task_result['num_files']} files")
            if task_result['stdout']:
                print("VTFCmd output:", task_result['stdout'])
            
            # Generate custom VMT files if enabled
            if context.scene.von_vmt_generate_bool:
                self._generate_vmt_files(context)
        else:
            error_msg = "VTFCmd failed"
            if task_result['stderr']:
                error_msg += f": {task_result['stderr']}"
            if task_result['stdout']:
                error_msg += f"\nOutput: {task_result['stdout']}"
            
            self.report({'ERROR'}, error_msg)
            print(f"VTFCmd command that failed: {task_result['command']}")
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def cancel(self, context):
        """Handle operator cancellation."""
        if self._timer:
            wm = context.window_manager
            wm.event_timer_remove(self._timer)
        if self._task_id:
            cleanup_task(self._task_id)
    
    def _generate_vmt_files(self, context):
        """Generate custom VMT files for each material."""
        scene = context.scene
        output_path = scene.von_material_output_path.path
        
        # Get the materials relative path
        materials_relative_path = get_materials_relative_path(output_path)
        
        # Global VMT parameters
        global_params = {
            'additive': scene.von_vmt_param_additive,
            'translucent': scene.von_vmt_param_translucent,
            'nocull': scene.von_vmt_param_nocull,
        }
        
        for mat_object in self._material_objects:
            try:
                # Determine texture paths for VMT
                base_texture_path = mat_object.material_name
                normal_texture_path = None
                phong_texture_path = None
                
                # Get additional texture paths
                if mat_object.material_name in self._all_additional_textures:
                    additional_textures = self._all_additional_textures[mat_object.material_name]
                    if 'normal' in additional_textures:
                        normal_name = os.path.splitext(os.path.basename(additional_textures['normal']))[0]
                        normal_texture_path = normal_name
                    
                    if 'phong' in additional_textures:
                        phong_name = os.path.splitext(os.path.basename(additional_textures['phong']))[0]
                        phong_texture_path = phong_name
                
                # Generate VMT content
                vmt_content = generate_vmt_content(
                    mat_object.material_name,
                    mat_object.vmt_params,
                    scene.von_vmt_shader,
                    base_texture_path,
                    normal_texture_path,
                    phong_texture_path,
                    materials_relative_path,
                    global_params
                )
                
                # Write VMT file
                write_vmt_file(output_path, mat_object.material_name, vmt_content)
                
            except Exception as e:
                self.report({'WARNING'}, f"Failed to generate VMT for {mat_object.material_name}: {e}")
                print(f"VMT generation error for {mat_object.material_name}: {e}")
        
        self.report({'INFO'}, f"Generated VMT files for {len(self._material_objects)} materials")


class VONVTF_OT_select_all_materials(Operator):
    """Select all materials in the list."""
    bl_idname = "von.vtf_select_all"
    bl_label = "Select All"
    bl_description = "Select all materials for conversion"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for item in context.scene.von_mats_collection:
            item.material_checkbox = True
        return {'FINISHED'}


class VONVTF_OT_deselect_all_materials(Operator):
    """Deselect all materials in the list."""
    bl_idname = "von.vtf_deselect_all"
    bl_label = "Deselect All"
    bl_description = "Deselect all materials"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for item in context.scene.von_mats_collection:
            item.material_checkbox = False
        return {'FINISHED'}


# ============================================================================
# Registration
# ============================================================================

CLASSES = [
    VONVTF_OT_refresh_materials,
    VONVTF_OT_convert_materials,
    VONVTF_OT_select_all_materials,
    VONVTF_OT_deselect_all_materials,
]


def register():
    """Register all classes."""
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister all classes."""
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
