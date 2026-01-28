"""
Path constants for addon data files.
"""
from pathlib import Path


def get_addon_directory() -> Path:
    """Get the root directory of this addon."""
    return Path(__file__).parent.parent


def get_data_directory() -> Path:
    """Get the addon's storeditems directory."""
    return get_addon_directory() / "storeditems"


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


# Specific file paths
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
