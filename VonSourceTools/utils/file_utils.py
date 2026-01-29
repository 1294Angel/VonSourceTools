"""
File I/O and path utilities.
"""
import json
from pathlib import Path

def load_json_data(relative_path: str, filename: str) -> dict:
    """
    Load JSON data from addon's storage directory.
    
    Args:
        relative_path: Path relative to addon root (e.g., "qcgenerator/templates")
        filename: JSON file name (e.g., "surfaceprops.json")
    
    Returns:
        dict: Loaded JSON data
    
    Raises:
        FileNotFoundError: If JSON file doesn't exist
    """
    addon_dir = Path(__file__).parent.parent  # Go up to addon root
    json_path = addon_dir / "storeditems" / relative_path / filename
    
    if not json_path.is_file():
        raise FileNotFoundError(f"JSON file not found: {json_path}")
    
    with json_path.open("r", encoding="utf-8") as f:
        return json.load(f)

def get_addon_directory() -> Path:
    """Get the root directory of this addon."""
    return Path(__file__).parent.parent

def get_data_directory() -> Path:
    """Get the addon's data storage directory."""
    return get_addon_directory() / "storeditems"