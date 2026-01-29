"""
Animation sequence collection and management.
"""
import bpy  # type: ignore


def collect_actions_from_armature(obj) -> set:
    """
    Collect all actions associated with an armature.
    
    Args:
        obj: The armature object
    
    Returns:
        set: Set of Action objects
    """
    actions = set()
    ad = obj.animation_data
    
    if not ad:
        return actions
    
    # Get active action
    if ad.action and isinstance(ad.action, bpy.types.Action):
        actions.add(ad.action)
    
    # Get actions from NLA tracks
    for track in ad.nla_tracks:
        for strip in track.strips:
            if strip.action and isinstance(strip.action, bpy.types.Action):
                actions.add(strip.action)
    
    return actions


def collect_sequences_from_selected(context) -> dict:
    """
    Collect animation sequences from all selected armatures.
    
    Args:
        context: Blender context
    
    Returns:
        dict: Dictionary mapping armature names to their actions
    """
    sequences = {}
    
    for obj in context.selected_objects:
        if obj.type != 'ARMATURE':
            continue
        
        actions = collect_actions_from_armature(obj)
        sequences[obj.name] = list(actions)
    
    return sequences


def populate_sequence_data(context) -> None:
    """
    Populate the scene's QC_PrimaryData with sequence information
    from selected armatures.
    
    Args:
        context: Blender context
    """
    primary_data = context.scene.QC_PrimaryData
    primary_data.sequence_objectdata.clear()
    
    for obj in context.selected_objects:
        if obj.type != 'ARMATURE':
            continue
        
        rig_data = primary_data.sequence_objectdata.add()
        rig_data.armatureName = obj.name
        
        actions = collect_actions_from_armature(obj)
        
        for action in actions:
            seq = rig_data.sequences.add()
            seq.originalName = action.name
            seq.sequenceName = action.name
