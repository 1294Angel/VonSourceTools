"""
SMD export utilities for batch exporting.
"""
import bpy  # type: ignore
import os


def split_objects_into_collections(context) -> dict:
    """
    Split all objects into temporary collections named original_objectname.
    
    Args:
        context: Blender context
    
    Returns:
        dict: Mapping of object names to their original and new collections
    """
    mapping = {}
    
    for obj in context.scene.objects:
        if not obj.users_collection:
            continue
        
        original_collections = list(obj.users_collection)
        new_collection_names = []
        
        for orig_col in original_collections:
            new_collection_name = f"{orig_col.name}_{obj.name}"
            new_collection_names.append(new_collection_name)
            
            if new_collection_name in bpy.data.collections:
                new_collection = bpy.data.collections[new_collection_name]
            else:
                new_collection = bpy.data.collections.new(new_collection_name)
                context.scene.collection.children.link(new_collection)
            
            if obj.name not in new_collection.objects:
                new_collection.objects.link(obj)
        
        for col in original_collections:
            if obj.name in col.objects:
                col.objects.unlink(obj)
        
        mapping[obj.name] = {
            'original': [col.name for col in original_collections],
            'new': new_collection_names
        }
    
    context.scene['_collection_split_mapping'] = mapping
    return mapping


def restore_objects_from_collections(context) -> None:
    """
    Restore objects to their original collections after splitting.
    
    Args:
        context: Blender context
    """
    mapping = context.scene.get('_collection_split_mapping')
    
    if not mapping:
        print("No mapping found. Nothing to restore.")
        return
    
    for obj_name, data in mapping.items():
        obj = context.scene.objects.get(obj_name)
        if not obj:
            continue
        
        # Unlink from temporary collections
        for new_col_name in data['new']:
            new_col = bpy.data.collections.get(new_col_name)
            if new_col and obj.name in new_col.objects:
                new_col.objects.unlink(obj)
                if len(new_col.objects) == 0:
                    bpy.data.collections.remove(new_col)
        
        # Link back to original collections
        for orig_col_name in data['original']:
            orig_col = bpy.data.collections.get(orig_col_name)
            if orig_col and obj.name not in orig_col.objects:
                orig_col.objects.link(obj)
            elif not orig_col:
                if obj.name not in context.scene.collection.objects:
                    context.scene.collection.objects.link(obj)
    
    del context.scene['_collection_split_mapping']


def export_scene_smd(context, export_folder: str) -> bool:
    """
    Export the scene to SMD format.
    
    Args:
        context: Blender context
        export_folder: Target folder for export
    
    Returns:
        bool: True if export dialog opened, False on error
    """
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    
    # Select all objects for export
    for obj in context.scene.objects:
        obj.select_set(True)
    
    try:
        bpy.ops.export_scene.smd('INVOKE_DEFAULT')
        return True
    except Exception as e:
        print(f"Export failed: {e}")
        return False
