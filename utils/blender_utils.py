"""
Blender-specific utility functions.
"""
import bpy  # type: ignore


def object_exists(name: str) -> bool:
    """
    Check if an object exists in the current blend file.
    
    Args:
        name: Name of the object to check
    
    Returns:
        bool: True if object exists, False otherwise
    """
    return name in bpy.data.objects


def move_to_collection(obj_name: str, collection_name: str) -> None:
    """
    Move an object to a specific collection, creating the collection if needed.
    
    Args:
        obj_name: Name of object to move
        collection_name: Name of target collection
    """
    obj = bpy.data.objects.get(obj_name)
    if not obj:
        raise ValueError(f"Object '{obj_name}' not found")
    
    # Get or create collection
    collection = bpy.data.collections.get(collection_name)
    if not collection:
        collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(collection)
    
    # Unlink from all current collections
    for coll in obj.users_collection:
        coll.objects.unlink(obj)
    
    # Link to target collection
    collection.objects.link(obj)


def select_objects(objects: list, active_object=None) -> None:
    """
    Select multiple objects and optionally set one as active.
    
    Args:
        objects: List of objects to select
        active_object: Object to set as active (optional)
    """
    bpy.ops.object.select_all(action='DESELECT')
    
    for obj in objects:
        obj.select_set(True)
    
    if active_object:
        bpy.context.view_layer.objects.active = active_object


def import_fbx(filepath: str) -> None:
    """
    Import an FBX file.
    
    Args:
        filepath: Path to the FBX file
    """
    bpy.ops.import_scene.fbx(filepath=filepath)


def get_armatures_in_scene() -> list:
    """
    Get all armature objects in the current scene.
    
    Returns:
        list: List of armature objects
    """
    return [obj for obj in bpy.data.objects if obj.type == 'ARMATURE']


def get_selected_armatures(context) -> list:
    """
    Get all selected armature objects.
    
    Args:
        context: Blender context
    
    Returns:
        list: List of selected armature objects
    """
    return [obj for obj in context.selected_objects if obj.type == 'ARMATURE']


def ensure_object_mode() -> None:
    """Ensure we're in object mode."""
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')


def clear_screen() -> None:
    """Print empty lines to clear console output."""
    for _ in range(5):
        print("")
