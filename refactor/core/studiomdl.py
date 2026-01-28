"""
StudioMDL compilation utilities.
"""
import subprocess
from pathlib import Path


def run_definebones(
    studiomdl_exe: Path,
    qc_path: Path,
    gmod_exe: Path,
    verbose: bool = False
) -> tuple:
    """
    Run studiomdl with -definebones flag.
    
    Args:
        studiomdl_exe: Path to studiomdl.exe
        qc_path: Path to the QC file
        gmod_exe: Path to Gmod.exe (used to get game folder)
        verbose: Whether to print output
    
    Returns:
        tuple: (stdout, stderr) from the process
    
    Raises:
        FileNotFoundError: If any required file doesn't exist
    """
    studiomdl_exe = Path(studiomdl_exe).resolve()
    qc_path = Path(qc_path).resolve()
    gmod_exe = Path(gmod_exe).resolve()
    
    if not studiomdl_exe.exists():
        raise FileNotFoundError(f"studiomdl.exe not found at {studiomdl_exe}")
    if not qc_path.exists():
        raise FileNotFoundError(f"QC file not found at {qc_path}")
    if not gmod_exe.exists():
        raise FileNotFoundError(f"Gmod.exe not found at {gmod_exe}")
    
    gmod_folder = gmod_exe.parent
    
    command = [
        str(studiomdl_exe),
        "-definebones",
        "-verbose",
        "-game", str(gmod_folder),
        str(qc_path)
    ]
    
    result = subprocess.run(
        command,
        cwd=studiomdl_exe.parent,
        capture_output=True,
        text=True
    )
    
    if verbose:
        print("=== STDOUT ===")
        print(result.stdout)
        print("=== STDERR ===")
        print(result.stderr)
    
    return result.stdout, result.stderr


def run_definebones_from_context(context) -> tuple:
    """
    Run definebones using settings from the toolbox.
    
    Args:
        context: Blender context
    
    Returns:
        tuple: (stdout, stderr) from the process
    """
    scene = context.scene
    toolbox = scene.toolBox
    
    return run_definebones(
        studiomdl_exe=toolbox.string_studiomdl_filelocation,
        qc_path=toolbox.string_qcGen_outputPath,
        gmod_exe=toolbox.string_gmodexe_path,
        verbose=toolbox.bool_studiomdl_verbose
    )
