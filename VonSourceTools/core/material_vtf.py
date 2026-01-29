"""
Core logic for Material to VTF conversion.

This module handles:
- Extracting textures from Blender materials
- Converting images to VTF format using VTFCmd
- Generating VMT files with Source Engine shader parameters
"""
import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


def get_image_texture_node(material) -> Optional[Any]:
    """
    Get the image texture node connected to the Principled BSDF base color.
    
    Args:
        material: Blender material object
        
    Returns:
        Image texture node if found, None otherwise
    """
    if not material.node_tree:
        return None
        
    # Find Principled BSDF node
    principled_node = None
    for node in material.node_tree.nodes:
        if node.type == 'BSDF_PRINCIPLED':
            principled_node = node
            break
            
    if not principled_node:
        return None
        
    # Check if Base Color input is linked
    base_color_input = principled_node.inputs.get("Base Color")
    if not base_color_input or not base_color_input.is_linked:
        return None
        
    # Find connected Image Texture node
    for link in base_color_input.links:
        from_node = link.from_node
        if from_node.type == 'TEX_IMAGE':
            return from_node
            
    return None


def validate_image_texture(image_node) -> Tuple[Optional[str], Optional[str]]:
    """
    Validate the image texture node and return image path.
    
    Args:
        image_node: Blender image texture node
        
    Returns:
        Tuple of (image_path, error_message). If successful, error_message is None.
    """
    import bpy
    
    if not image_node.image:
        return None, "No source image found"
        
    if image_node.image.is_dirty:
        return None, "There are unsaved changes to your source image. Please save it first"
        
    image_path_raw = image_node.image.filepath_raw
    if not image_path_raw:
        return None, "Image has no file path (may be generated or packed)"
        
    # Convert to readable absolute path
    full_abs_path = bpy.path.abspath(image_path_raw)
    real_abs_path = os.path.realpath(full_abs_path)
    
    if not os.path.exists(real_abs_path):
        return None, f"Image file not found: {real_abs_path}"
        
    return real_abs_path, None


def get_materials_relative_path(material_output_path: str) -> str:
    """
    Extract the path relative to the 'materials' folder.
    
    Args:
        material_output_path: Full output path
        
    Returns:
        Path relative to materials folder, or empty string if not found
    """
    # Normalize the path separators
    normalized_path = material_output_path.replace('\\', '/')
    
    # Find the 'materials' folder in the path
    materials_index = normalized_path.lower().find('/materials/')
    if materials_index == -1:
        # Try without leading slash
        materials_index = normalized_path.lower().find('materials/')
        if materials_index == -1:
            return ""  # No materials folder found, use empty path
        else:
            start_index = materials_index + len('materials/')
    else:
        start_index = materials_index + len('/materials/')
    
    # Extract everything after 'materials/'
    relative_path = normalized_path[start_index:]
    
    # Remove trailing slash if present
    relative_path = relative_path.rstrip('/')
    
    return relative_path


def process_additional_textures(
    material_name: str,
    vmt_params,
    material_output_path: str
) -> Dict[str, str]:
    """
    Process normal maps and other additional textures for a material.
    
    Args:
        material_name: Name of the material
        vmt_params: VMT parameters property group
        material_output_path: Output directory path
        
    Returns:
        Dictionary mapping texture type to file path
    """
    import bpy
    
    additional_textures = {}
    
    # Process normal map
    if vmt_params.normal_map:
        normal_image = vmt_params.normal_map
        if normal_image.filepath_raw:
            normal_path_raw = normal_image.filepath_raw
            normal_full_path = bpy.path.abspath(normal_path_raw)
            normal_real_path = os.path.realpath(normal_full_path)
            
            if os.path.exists(normal_real_path):
                # Copy and convert normal map
                image_root, image_ext = os.path.splitext(normal_real_path)
                normal_name = f"{material_name}_n{image_ext}"
                normal_copy_path = os.path.join(os.path.dirname(normal_real_path), normal_name)
                
                # Only copy if source and destination are different
                src_normalized = os.path.normpath(normal_real_path)
                dst_normalized = os.path.normpath(normal_copy_path)
                
                if src_normalized != dst_normalized:
                    try:
                        shutil.copy2(normal_real_path, normal_copy_path)
                    except Exception as e:
                        print(f"Failed to copy normal map for {material_name}: {e}")
                
                additional_textures['normal'] = normal_copy_path
    
    # Process phong exponent map
    if vmt_params.phong_exponent_map:
        phong_image = vmt_params.phong_exponent_map
        if phong_image.filepath_raw:
            phong_path_raw = phong_image.filepath_raw
            phong_full_path = bpy.path.abspath(phong_path_raw)
            phong_real_path = os.path.realpath(phong_full_path)
            
            if os.path.exists(phong_real_path):
                # Copy and convert phong exponent map
                image_root, image_ext = os.path.splitext(phong_real_path)
                phong_name = f"{material_name}_e{image_ext}"
                phong_copy_path = os.path.join(os.path.dirname(phong_real_path), phong_name)
                
                # Only copy if source and destination are different
                src_normalized = os.path.normpath(phong_real_path)
                dst_normalized = os.path.normpath(phong_copy_path)
                
                if src_normalized != dst_normalized:
                    try:
                        shutil.copy2(phong_real_path, phong_copy_path)
                    except Exception as e:
                        print(f"Failed to copy phong exponent map for {material_name}: {e}")
                
                additional_textures['phong'] = phong_copy_path
    
    return additional_textures


def generate_vmt_content(
    material_name: str,
    vmt_params,
    shader_type: str,
    base_texture_path: str,
    normal_texture_path: Optional[str] = None,
    phong_texture_path: Optional[str] = None,
    materials_relative_path: str = "",
    global_params: Optional[Dict[str, bool]] = None
) -> str:
    """
    Generate VMT file content based on parameters.
    
    Args:
        material_name: Name of the material
        vmt_params: VMT parameters property group
        shader_type: Source Engine shader type
        base_texture_path: Path to base texture
        normal_texture_path: Path to normal map (optional)
        phong_texture_path: Path to phong exponent map (optional)
        materials_relative_path: Path relative to materials folder
        global_params: Global VMT parameters (additive, translucent, nocull)
        
    Returns:
        VMT file content as string
    """
    # Build full texture paths with materials relative path
    if materials_relative_path:
        full_base_path = f"{materials_relative_path}/{base_texture_path}"
        full_normal_path = f"{materials_relative_path}/{normal_texture_path}" if normal_texture_path else None
        full_phong_path = f"{materials_relative_path}/{phong_texture_path}" if phong_texture_path else None
    else:
        full_base_path = base_texture_path
        full_normal_path = normal_texture_path
        full_phong_path = phong_texture_path
    
    # Start VMT content
    vmt_content = f'"{shader_type}"\n{{\n'
    
    # Base texture (always required)
    vmt_content += f'    "$basetexture" "{full_base_path}"\n'
    
    # Normal map
    if full_normal_path and vmt_params.normal_map:
        vmt_content += f'    "$bumpmap" "{full_normal_path}"\n'
    
    # Phong exponent texture
    if full_phong_path and vmt_params.phong_exponent_map:
        vmt_content += f'    "$phongexponenttexture" "{full_phong_path}"\n'
    
    # Fixed parameters
    vmt_content += '    /////////////////\n'
    color2_str = f"[{vmt_params.color2[0]:.3f} {vmt_params.color2[1]:.3f} {vmt_params.color2[2]:.3f}]"
    vmt_content += f'    "$color2" "{color2_str}"                                     //do not touch this\n'
    
    if vmt_params.blend_tint_by_base_alpha:
        vmt_content += '    "$blendtintbybasealpha" "1"                             //do not touch this\n'
    
    vmt_content += '    /////////////////\n'
    
    # Phong parameters
    if vmt_params.enable_phong:
        vmt_content += '    "$phong" "1"\n'
        vmt_content += f'    "$phongboost" "{vmt_params.phong_boost:.1f}"\n'
        
        if vmt_params.phong_albedo_tint:
            vmt_content += '    "$phongalbedotint" "1"\n'
        
        vmt_content += f'    "$phongalbedoboost" "{vmt_params.phong_albedo_boost:.0f}"                                //toy around with this\n'
        
        fresnel_str = f"[{vmt_params.phong_fresnel_ranges[0]:.1f} {vmt_params.phong_fresnel_ranges[1]:.1f} {vmt_params.phong_fresnel_ranges[2]:.1f}]"
        vmt_content += f'    "$phongfresnelranges" "{fresnel_str}"\n'
    
    # Rim lighting
    if vmt_params.enable_rimlight:
        vmt_content += '    //rimlight doesn\'t properly show in hlmv, make sure you\'re changing these values in game\n'
        vmt_content += '    "$rimlight" "1"\n'
        vmt_content += f'    "$rimlightexponent" "{vmt_params.rimlight_exponent:.0f}"\n'
        
        if vmt_params.rim_mask:
            vmt_content += '    "$rimmask" "1"\n'
        
        vmt_content += f'    "$rimlightboost" "{vmt_params.rimlight_boost:.1f}"\n'
    
    vmt_content += '       \n'
    vmt_content += '    /////////////////\n'
    
    # Normal map alpha environment mask
    if vmt_params.normal_map_alpha_envmap_mask and full_normal_path:
        vmt_content += '    "$normalmapalphaenvmapmask" "1"                         //do not touch this\n'
    
    vmt_content += '    /////////////////\n'
    
    # Environment mapping
    if vmt_params.enable_envmap:
        vmt_content += '    "$envmap" "env_cubemap"\n'
        envmap_tint_str = f"[{vmt_params.envmap_tint[0]:.3f} {vmt_params.envmap_tint[1]:.3f} {vmt_params.envmap_tint[2]:.3f}]"
        vmt_content += f'    "$envmaptint" "{envmap_tint_str}"                 \n'
    
    # Global VMT parameters
    if global_params:
        if global_params.get('additive'):
            vmt_content += '    "$additive" "1"\n'
        if global_params.get('translucent'):
            vmt_content += '    "$translucent" "1"\n'
        if global_params.get('nocull'):
            vmt_content += '    "$nocull" "1"\n'
    
    vmt_content += '}\n'
    
    return vmt_content


def write_vmt_file(output_path: str, material_name: str, vmt_content: str) -> str:
    """
    Write VMT file to disk.
    
    Args:
        output_path: Directory to write to
        material_name: Name of the material (used for filename)
        vmt_content: VMT file content
        
    Returns:
        Full path to written VMT file
    """
    vmt_filename = f"{material_name}.vmt"
    vmt_filepath = os.path.join(output_path, vmt_filename)
    
    with open(vmt_filepath, 'w', encoding='utf-8') as vmt_file:
        vmt_file.write(vmt_content)
    
    print(f"Generated VMT file: {vmt_filepath}")
    return vmt_filepath


def build_vtfcmd_command(
    vtfcmd_exe: str,
    image_paths: List[str],
    image_name_mapping: Dict[str, str],
    output_path: str,
    vtf_format: str = 'dxt5',
    alpha_format: str = 'dxt5',
    vtf_version: str = '7.5',
    resize: bool = False,
    resize_method: str = 'BIGGEST',
    resize_filter: str = 'TRIANGLE',
    clamp_size: str = '512x512',
    shader: Optional[str] = None,
    vmt_params: Optional[Dict[str, bool]] = None,
    additional_texture_paths: Optional[Dict[str, List[str]]] = None
) -> List[str]:
    """
    Build the VTFCmd command line arguments.
    
    Args:
        vtfcmd_exe: Path to VTFCmd.exe
        image_paths: List of image file paths to convert
        image_name_mapping: Mapping of image paths to material names
        output_path: Output directory for VTF files
        vtf_format: Texture compression format
        alpha_format: Alpha channel compression format
        vtf_version: VTF file format version
        resize: Whether to resize images
        resize_method: Resize method
        resize_filter: Resize filter algorithm
        clamp_size: Maximum texture dimensions
        shader: Shader type for VMT generation (None to skip VMT)
        vmt_params: VMT parameters (additive, translucent, nocull)
        additional_texture_paths: Additional textures to process
        
    Returns:
        List of command line arguments
    """
    # Validate paths
    if not os.path.exists(vtfcmd_exe):
        raise FileNotFoundError(f"VTFCmd.exe not found at: {vtfcmd_exe}")
    if not os.path.exists(output_path):
        raise FileNotFoundError(f"Material output folder not found: {output_path}")
    
    # Start with executable
    command_line = [vtfcmd_exe]
    
    # Process base textures
    for image_path in image_paths:
        # Copy image with material name
        image_root, image_ext = os.path.splitext(image_path)
        material_name = image_name_mapping[image_path]
        new_image_path = os.path.join(
            os.path.dirname(image_path), 
            material_name + image_ext
        )
        
        # Only copy if source and destination are different
        # Normalize paths for comparison
        src_normalized = os.path.normpath(os.path.realpath(image_path))
        dst_normalized = os.path.normpath(os.path.realpath(new_image_path))
        
        if src_normalized != dst_normalized:
            try:
                shutil.copy2(image_path, new_image_path)
            except Exception as e:
                raise IOError(f"Failed to copy image: {e}")
        
        command_line.extend(["-file", new_image_path])
    
    # Process additional textures
    additional_files_command = []
    if additional_texture_paths:
        for texture_type, texture_paths in additional_texture_paths.items():
            for texture_path in texture_paths:
                additional_files_command.extend(["-file", texture_path])
    
    # Add format parameters
    command_line.extend(["-format", vtf_format])
    command_line.extend(["-alphaformat", alpha_format])
    command_line.extend(["-version", vtf_version])
    
    # Add resize parameters if enabled
    if resize:
        command_line.append("-resize")
        command_line.extend(["-rmethod", resize_method])
        command_line.extend(["-rfilter", resize_filter])
        
        clamp_value = clamp_size.split('x')[0]
        command_line.extend(["-rclampwidth", clamp_value])
        command_line.extend(["-rclampheight", clamp_value])
    
    # Add VMT shader parameters if enabled
    if shader:
        command_line.extend(["-shader", shader])
        
        if vmt_params:
            if vmt_params.get('additive'):
                command_line.extend(["-param", "additive", "1"])
            if vmt_params.get('translucent'):
                command_line.extend(["-param", "translucent", "1"])
            if vmt_params.get('nocull'):
                command_line.extend(["-param", "nocull", "1"])
    
    # Set output folder
    command_line.extend(["-output", output_path.rstrip(os.sep)])
    
    # Add additional texture files
    command_line.extend(additional_files_command)
    
    return command_line


def execute_vtfcmd(command_line: List[str]) -> Tuple[bool, str, str]:
    """
    Execute VTFCmd with the given arguments.
    
    Args:
        command_line: List of command line arguments
        
    Returns:
        Tuple of (success, stdout, stderr)
    """
    try:
        process = subprocess.Popen(
            command_line,
            stdin=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=False,
            text=True
        )
        
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            return True, stdout, stderr
        else:
            return False, stdout, stderr
            
    except Exception as e:
        return False, "", str(e)


def collect_scene_materials(context) -> List[Any]:
    """
    Collect all materials from scene objects.
    
    Args:
        context: Blender context
        
    Returns:
        List of (material_slot, material) tuples
    """
    mats_set = set()
    materials = []
    
    for obj in context.scene.objects:
        if hasattr(obj, 'material_slots'):
            for material_slot in obj.material_slots:
                if (material_slot.material and 
                    material_slot.material.name not in mats_set and 
                    material_slot.material.users > 0):
                    mats_set.add(material_slot.material.name)
                    materials.append(material_slot)
    
    return materials
