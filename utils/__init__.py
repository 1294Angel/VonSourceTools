"""
Utilities module - Contains utility functions for VonSourceTools.
"""
from .blender_utils import (
    object_exists,
    move_to_collection,
    select_objects,
    import_fbx,
    get_armatures_in_scene,
    get_selected_armatures,
    ensure_object_mode,
    clear_screen,
)
from .file_utils import (
    load_json_data,
    get_addon_directory,
    get_data_directory,
)
from .threading_utils import (
    TaskStatus,
    TaskResult,
    BackgroundTask,
    TaskManager,
    task_manager,
    run_in_background,
    get_task_result,
    is_task_finished,
    cleanup_task,
)

__all__ = [
    # Blender utilities
    'object_exists',
    'move_to_collection',
    'select_objects',
    'import_fbx',
    'get_armatures_in_scene',
    'get_selected_armatures',
    'ensure_object_mode',
    'clear_screen',
    # File utilities
    'load_json_data',
    'get_addon_directory',
    'get_data_directory',
    # Threading utilities
    'TaskStatus',
    'TaskResult',
    'BackgroundTask',
    'TaskManager',
    'task_manager',
    'run_in_background',
    'get_task_result',
    'is_task_finished',
    'cleanup_task',
]
