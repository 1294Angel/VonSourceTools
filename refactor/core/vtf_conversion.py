"""
VTF (Valve Texture Format) batch conversion utilities.
"""
import subprocess
from pathlib import Path


def convert_file_with_structure(
    file_path: Path,
    export_format: str,
    input_folder: Path,
    output_folder: Path,
    vtfcmd_exe: Path
) -> bool:
    """
    Convert a single file while preserving folder structure.
    
    Args:
        file_path: Path to the source file
        export_format: Target format (e.g., "vtf", "png", "tga")
        input_folder: Root input folder
        output_folder: Root output folder
        vtfcmd_exe: Path to VTFCmd.exe
    
    Returns:
        bool: True if conversion succeeded, False otherwise
    """
    relative_path = file_path.relative_to(input_folder)
    output_subfolder = output_folder / relative_path.parent
    output_subfolder.mkdir(parents=True, exist_ok=True)
    output_path = output_subfolder / (file_path.stem + f".{export_format}")
    
    cmd = [
        str(vtfcmd_exe),
        "-file", str(file_path),
        "-output", str(output_subfolder),
        "-exportformat", export_format,
        "-silent"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Converted: {file_path} -> {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed: {file_path}, {e}")
        return False


def batch_convert(context) -> tuple:
    """
    Batch convert image files based on toolbox settings.
    
    Args:
        context: Blender context
    
    Returns:
        tuple: (success_count, failure_count)
    """
    scene = context.scene
    toolbox = scene.toolBox
    
    vtfcmd_exe = Path(toolbox.string_vtfbatch_vtfccmdexe)
    input_folder = Path(toolbox.string_vtfbatch_inputfolder)
    output_folder = Path(toolbox.string_vtfbatch_outputfolder)
    source_filetype = toolbox.enum_vtfbatch_sourcefiletype
    target_filetype = toolbox.enum_vtfbatch_targetfiletype
    
    if not input_folder.exists():
        print(f"Input folder '{input_folder}' does not exist.")
        return (0, 0)
    
    files = list(input_folder.rglob(f"*.{source_filetype}"))
    
    if not files:
        print(f"No *.{source_filetype} files found in '{input_folder}' folder.")
        return (0, 0)
    
    success_count = 0
    failure_count = 0
    
    for file in files:
        if convert_file_with_structure(
            file, target_filetype, input_folder, output_folder, vtfcmd_exe
        ):
            success_count += 1
        else:
            failure_count += 1
    
    print(f"Batch conversion completed! Success: {success_count}, Failed: {failure_count}")
    return (success_count, failure_count)


# Supported file types for conversion
SUPPORTED_FILETYPES = [
    ("png", ".png", "PNG image"),
    ("jpg", ".jpg", "JPG/JPEG image"),
    ("jpeg", ".jpeg", "JPEG image"),
    ("tga", ".tga", "TGA image"),
    ("bmp", ".bmp", "BMP image"),
    ("psd", ".psd", "Photoshop PSD file"),
    ("hdr", ".hdr", "HDR image"),
    ("exr", ".exr", "OpenEXR image"),
    ("vtf", ".vtf", "VTF file (Valve Texture Format)")
]


def get_supported_filetypes() -> list:
    """
    Get the list of supported file types for conversion.
    
    Returns:
        list: List of tuples (id, display, description)
    """
    return SUPPORTED_FILETYPES
