"""
Path constants for addon data files.

IMPORTANT: External tool paths are configured here.
If you need to change tool locations, modify the variables below.
"""
from pathlib import Path


# ============================================================================
# EXTERNAL TOOL PATHS - MODIFY THESE IF NEEDED
# ============================================================================

# VTFCmd.exe location - Set this to your VTFCmd installation path
# Default: looks in addon's "storeditems/external_software_dependancies/vtfcmd" folder
# You can change this to an absolute path if VTFCmd is installed elsewhere
# Example: VTFCMD_PATH = Path("C:/Program Files/VTFEdit/VTFCmd.exe")
VTFCMD_PATH = Path(__file__).parent.parent / "tools" / "vtfcmd" / "VTFCmd.exe"

# StudioMDL path - typically found in your Source SDK bin folder
# Default: looks in addon's "storeditems/external_software_dependancies/studiomdl/bin" folder
# Example: STUDIOMDL_PATH = Path("C:/Program Files (x86)/Steam/steamapps/common/Team Fortress 2/bin/studiomdl.exe")
STUDIOMDL_PATH = Path(__file__).parent.parent / "tools" / "studiomdl" / "bin" / "studiomdl.exe"


# ============================================================================
# Addon Directory Functions
# ============================================================================

def get_addon_directory() -> Path:
    """Get the root directory of this addon."""
    return Path(__file__).parent.parent


def get_data_directory() -> Path:
    """Get the addon's storeditems directory."""
    return get_addon_directory() / "storeditems"


def get_external_software_directory() -> Path:
    """Get the addon's external software dependencies directory."""
    return get_data_directory() / "external_software_dependancies"


def get_tools_directory() -> Path:
    """Get the addon's tools directory for bundled executables (legacy)."""
    return get_addon_directory() / "tools"


def get_deltaanimtrick_directory() -> Path:
    """Get the delta animation trick data directory."""
    return get_data_directory() / "deltaanimtrick"


def get_qcgenerator_directory() -> Path:
    """Get the QC generator data directory."""
    return get_data_directory() / "qcgenerator"


def get_templates_directory() -> Path:
    """Get the QC templates directory."""
    return get_qcgenerator_directory() / "templates"


def get_commands_directory() -> Path:
    """Get the QC command templates directory."""
    return get_templates_directory() / "commands"


# ============================================================================
# Default External Tool Paths
# ============================================================================

def get_default_vtfcmd_path() -> str:
    """
    Get the default path to VTFCmd.exe for UI property defaults.
    
    Returns:
        String path to the expected VTFCmd location
    """
    return str(get_external_software_directory() / "vtfcmd" / "VTFCmd.exe")


def get_default_studiomdl_path() -> str:
    """
    Get the default path to studiomdl.exe for UI property defaults.
    
    Returns:
        String path to the expected studiomdl location
    """
    return str(get_external_software_directory() / "studiomdl" / "bin" / "studiomdl.exe")


# ============================================================================
# External Tool Path Functions
# ============================================================================

def get_vtfcmd_path() -> Path:
    """
    Get the path to VTFCmd.exe.
    
    Resolution order:
    1. VTFCMD_PATH constant if set (at top of this file)
    2. Bundled version in addon's storeditems/external_software_dependancies/vtfcmd folder
    3. Legacy location in addon's tools/vtfcmd folder
    4. Returns None if not found (UI path will be used)
    
    Returns:
        Path to VTFCmd.exe or None if not found
    """
    # Check if constant is set
    if VTFCMD_PATH is not None:
        vtfcmd = Path(VTFCMD_PATH)
        if vtfcmd.exists():
            return vtfcmd
    
    # Check new bundled version location
    bundled_vtfcmd = get_external_software_directory() / "vtfcmd" / "VTFCmd.exe"
    if bundled_vtfcmd.exists():
        return bundled_vtfcmd
    
    # Check legacy location
    legacy_vtfcmd = get_tools_directory() / "vtfcmd" / "VTFCmd.exe"
    if legacy_vtfcmd.exists():
        return legacy_vtfcmd
    
    # Not found - will need to use UI path
    return None


def get_studiomdl_path() -> Path:
    """
    Get the path to studiomdl.exe.
    
    Resolution order:
    1. STUDIOMDL_PATH constant if set (at top of this file)
    2. Bundled version in addon's storeditems/external_software_dependancies/studiomdl/bin folder
    3. Legacy location in addon's tools/studiomdl folder
    4. Returns None if not found (UI path will be used)
    
    Returns:
        Path to studiomdl.exe or None if not found
    """
    # Check if constant is set
    if STUDIOMDL_PATH is not None:
        studiomdl = Path(STUDIOMDL_PATH)
        if studiomdl.exists():
            return studiomdl
    
    # Check new bundled version location
    bundled_studiomdl = get_external_software_directory() / "studiomdl" / "bin" / "studiomdl.exe"
    if bundled_studiomdl.exists():
        return bundled_studiomdl
    
    # Check legacy location
    legacy_studiomdl = get_tools_directory() / "studiomdl" / "studiomdl.exe"
    if legacy_studiomdl.exists():
        return legacy_studiomdl
    
    # Not found - will need to use UI path
    return None


def is_studiomdl_bundled() -> bool:
    """
    Check if StudioMDL is available from bundled or configured path.
    
    Returns:
        True if StudioMDL is available, False otherwise
    """
    return get_studiomdl_path() is not None


def is_vtfcmd_bundled() -> bool:
    """
    Check if VTFCmd is available from bundled or configured path.
    
    Returns:
        True if VTFCmd is available, False otherwise
    """
    return get_vtfcmd_path() is not None


# ============================================================================
# Specific File Paths
# ============================================================================

def get_surfaceprops_path() -> Path:
    """Get the surfaceprops.json file path."""
    return get_templates_directory() / "surfaceprops.json"


def get_activities_path() -> Path:
    """Get the activities.json file path."""
    return get_templates_directory() / "activities.json"


def get_qc_section_order_path() -> Path:
    """Get the qc_section_order.json file path."""
    return get_templates_directory() / "qc_section_order.json"


def get_armature_file_locations() -> dict:
    """
    Get the paths to delta animation trick armature files.
    
    Returns:
        dict: Dictionary mapping armature names to their file paths
    """
    base_dir = get_deltaanimtrick_directory()
    return {
        "proportions": base_dir / "proportions.fbx",
        "reference_female": base_dir / "reference_female.fbx",
        "reference_male": base_dir / "reference_male.fbx"
    }
