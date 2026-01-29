"""
Data module - Contains static data, constants, and path utilities.
"""
from .constants import MODEL_TYPE_CATEGORY_MAP, NONE_ENUM
from .valvebiped_bones import VALVEBIPED_BONES, VALVEBIPED_CONSTRAINT_PAIRS
from .paths import (
    get_addon_directory,
    get_data_directory,
    get_deltaanimtrick_directory,
    get_qcgenerator_directory,
    get_templates_directory,
    get_commands_directory,
    get_surfaceprops_path,
    get_activities_path,
    get_qc_section_order_path,
    get_armature_file_locations,
)

__all__ = [
    # Constants
    'MODEL_TYPE_CATEGORY_MAP',
    'NONE_ENUM',
    # Bone data
    'VALVEBIPED_BONES',
    'VALVEBIPED_CONSTRAINT_PAIRS',
    # Path utilities
    'get_addon_directory',
    'get_data_directory',
    'get_deltaanimtrick_directory',
    'get_qcgenerator_directory',
    'get_templates_directory',
    'get_commands_directory',
    'get_surfaceprops_path',
    'get_activities_path',
    'get_qc_section_order_path',
    'get_armature_file_locations',
]
