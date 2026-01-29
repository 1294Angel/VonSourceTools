"""
QC file generation logic.

This module generates QC files for Source Engine models using:
- Properties gathered from the UI panels
- Templates from storeditems/qcgenerator/templates/commands/
- Section ordering from qc_section_order.json
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

# Import bpy conditionally for type hints and actual use
try:
    import bpy  # type: ignore
except ImportError:
    bpy = None

from ..data.paths import get_templates_directory, get_commands_directory


# ============================================================================
# Data Classes for QC Generation
# ============================================================================

@dataclass
class QCData:
    """Container for all QC generation data gathered from UI."""
    # Basic info
    model_type: str = "PROP"
    model_name: str = ""
    output_path: str = ""
    
    # Scale and positioning
    scale: int = 1
    origin: tuple = (0, 0, 0)
    
    # Materials
    material_paths: List[str] = field(default_factory=list)
    
    # Surface properties
    surfaceprop: str = "default"
    
    # Collision
    generate_collision: bool = False
    collision_collection: str = ""
    collision_mass: float = 50.0
    collision_concave: bool = False
    
    # Bodygroups: {name: [collection_names]}
    bodygroups: Dict[str, List[str]] = field(default_factory=dict)
    
    # Sequences: [{name, file, fps, activity, activity_weight}]
    sequences: List[Dict[str, Any]] = field(default_factory=list)
    
    # Attachments: [{name, bone, position}]
    attachments: List[Dict[str, Any]] = field(default_factory=list)
    
    # Includes
    include_files: List[str] = field(default_factory=list)
    
    # Flags
    staticprop: bool = False
    
    # Character-specific
    include_default_anims: str = "None"  # None, f_anm.mdl, m_anm.mdl, z_anm.mdl
    definebones: bool = False


# ============================================================================
# Template Loading
# ============================================================================

def load_template(template_name: str) -> str:
    """
    Load a QC command template.
    
    Args:
        template_name: Name of the template file (without .txt extension)
    
    Returns:
        Template content as string
    """
    template_path = get_commands_directory() / f"{template_name}.txt"
    
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    
    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Normalize line endings
    return content.replace('\r\n', '\n').replace('\r', '\n')


def load_section_order(model_type: str) -> Dict[str, Any]:
    """
    Load the section order configuration for a model type.
    
    Args:
        model_type: Type of model (PROP, CHARACTER, NPC, etc.)
    
    Returns:
        Dictionary with 'sections' and 'flags' lists
    """
    json_path = get_templates_directory() / "qc_section_order.json"
    
    if not json_path.exists():
        raise FileNotFoundError(f"Section order config not found: {json_path}")
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    model_type_upper = model_type.upper()
    if model_type_upper not in data:
        raise ValueError(f"Unknown model type: {model_type}")
    
    return data[model_type_upper]


# ============================================================================
# QC Section Generators
# ============================================================================

def generate_modelname(qc_data: QCData) -> str:
    """Generate $modelname command."""
    if not qc_data.model_name:
        return ""
    
    template = load_template("modelname")
    return template.format(mdlModelName=qc_data.model_name)


def generate_scale(qc_data: QCData) -> str:
    """Generate $scale command."""
    if qc_data.scale == 1:
        return ""  # Default scale, not needed
    
    template = load_template("scale")
    return template.format(scale=qc_data.scale)


def generate_origin(qc_data: QCData) -> str:
    """Generate $origin command."""
    x, y, z = qc_data.origin
    if x == 0 and y == 0 and z == 0:
        return ""  # Default origin, not needed
    
    template = load_template("origin")
    return template.format(x=x, y=y, z=z)


def generate_surfaceprop(qc_data: QCData) -> str:
    """Generate $surfaceprop command."""
    if not qc_data.surfaceprop:
        return ""
    
    template = load_template("surfaceprop")
    return template.format(surfaceProp=qc_data.surfaceprop)


def generate_cdmaterials(qc_data: QCData) -> str:
    """Generate $cdmaterials commands."""
    if not qc_data.material_paths:
        return ""
    
    template = load_template("cdmaterials")
    lines = []
    
    for path in qc_data.material_paths:
        # Clean up the path
        clean_path = path.replace("\\", "/").strip("/")
        lines.append(template.format(materialPath=clean_path))
    
    return "\n".join(lines)


def generate_bodygroups(qc_data: QCData) -> str:
    """Generate $bodygroup commands."""
    if not qc_data.bodygroups:
        return ""
    
    template = load_template("bodygroup")
    sections = []
    
    for bg_name, collections in qc_data.bodygroups.items():
        # Build bodygroup lines
        bg_lines = []
        for collection_name in collections:
            # Each collection becomes a studio line
            # The SMD filename is assumed to be the collection name
            bg_lines.append(f'    studio "{collection_name}.smd"')
        
        # Add blank option if there's more than one option
        if len(collections) > 0:
            bg_lines.append('    blank')
        
        bodygroup_content = template.format(
            bodygroupName=bg_name,
            bodygroupLines="\n".join(bg_lines)
        )
        sections.append(bodygroup_content)
    
    return "\n".join(sections)


def generate_sequences(qc_data: QCData) -> str:
    """Generate $sequence commands."""
    if not qc_data.sequences:
        # Default idle sequence for props
        if qc_data.model_type == "PROP":
            return '$sequence "idle" "idle.smd" fps 1'
        return ""
    
    lines = []
    
    for seq in qc_data.sequences:
        seq_name = seq.get("name", "idle")
        seq_file = seq.get("file", seq_name)
        fps = seq.get("fps", 30)
        activity = seq.get("activity", "")
        activity_weight = seq.get("activity_weight", 1)
        
        # Build the sequence line
        line = f'$sequence "{seq_name}" "{seq_file}.smd" fps {fps}'
        
        # Add activity if specified
        if activity and activity != "NONE":
            line += f' activity "{activity}" {activity_weight}'
        
        lines.append(line)
    
    return "\n".join(lines)


def generate_collisionmodel(qc_data: QCData) -> str:
    """Generate $collisionmodel command."""
    # Determine collision file
    if qc_data.generate_collision:
        collision_file = f"{qc_data.model_name}_phys.smd"
    elif qc_data.collision_collection:
        collision_file = f"{qc_data.collision_collection}.smd"
    else:
        return ""
    
    # Build collision options
    options = []
    options.append(f"    $mass {qc_data.collision_mass}")
    
    if qc_data.collision_concave:
        options.append("    $concave")
    
    return f'$collisionmodel "{collision_file}" {{\n' + "\n".join(options) + "\n}"


def generate_attachments(qc_data: QCData) -> str:
    """Generate $attachment commands."""
    if not qc_data.attachments:
        return ""
    
    template = load_template("attachment")
    lines = []
    
    for att in qc_data.attachments:
        name = att.get("name", "attachment")
        bone = att.get("bone", "root")
        pos = att.get("position", (0, 0, 0))
        
        line = template.format(
            attachmentName=name,
            boneName=bone,
            x=pos[0],
            y=pos[1],
            z=pos[2]
        )
        lines.append(line)
    
    return "\n".join(lines)


def generate_includes(qc_data: QCData) -> str:
    """Generate $include commands."""
    if not qc_data.include_files:
        return ""
    
    template = load_template("include")
    lines = []
    
    for filename in qc_data.include_files:
        # Remove .qc extension if present (template adds it)
        clean_name = filename.replace(".qc", "").replace(".qci", "")
        lines.append(template.format(fileName=clean_name))
    
    return "\n".join(lines)


def generate_includemodel(qc_data: QCData) -> str:
    """Generate $includemodel command for character animations."""
    if qc_data.include_default_anims == "None":
        return ""
    
    return f'$includemodel "{qc_data.include_default_anims}"'


def generate_staticprop(qc_data: QCData) -> str:
    """Generate $staticprop flag."""
    if qc_data.staticprop:
        return "$staticprop"
    return ""


def generate_illumposition(qc_data: QCData) -> str:
    """Generate $illumposition command."""
    # Default illumination position at model center
    # This can be enhanced later with actual calculated positions
    return ""


# ============================================================================
# Section Dispatcher
# ============================================================================

SECTION_GENERATORS = {
    "modelname": generate_modelname,
    "scale": generate_scale,
    "origin": generate_origin,
    "surfaceprop": generate_surfaceprop,
    "cdmaterials": generate_cdmaterials,
    "bodygroup": generate_bodygroups,
    "sequence": generate_sequences,
    "collisionmodel": generate_collisionmodel,
    "attachment": generate_attachments,
    "include": generate_includes,
    "illumposition": generate_illumposition,
}

FLAG_GENERATORS = {
    "staticprop": generate_staticprop,
    "includemodel": generate_includemodel,
}


# ============================================================================
# Data Gathering from Blender
# ============================================================================

def gather_qc_data_from_scene(context) -> QCData:
    """
    Gather all QC data from Blender scene properties.
    
    Args:
        context: Blender context
    
    Returns:
        QCData object with all gathered data
    """
    scene = context.scene
    toolbox = scene.toolBox
    qc_primary = scene.QC_PrimaryData
    
    qc_data = QCData()
    
    # Basic info
    qc_data.model_type = toolbox.enum_qcGen_modelType
    qc_data.model_name = toolbox.string_qcGen_mdlModelName
    qc_data.output_path = toolbox.string_qcGen_outputPath
    
    # Scale
    qc_data.scale = toolbox.int_qcGen_scale
    
    # Surface property
    surfaceprop = getattr(toolbox, 'enum_surfaceprop_item', '')
    if surfaceprop and surfaceprop != 'NONE':
        qc_data.surfaceprop = surfaceprop
    
    # Collision
    qc_data.generate_collision = toolbox.bool_qcGen_generateCollission
    qc_data.collision_collection = toolbox.string_qcGen_existingCollissionCollection
    
    # Material paths (cdmaterials)
    qc_data.material_paths = []
    for vmt_item in qc_primary.vmt_filepaths:
        if vmt_item.filepath:
            # Extract the path relative to materials folder
            path = vmt_item.filepath
            # Try to find 'materials' in the path and get everything after
            if 'materials' in path.lower():
                idx = path.lower().find('materials')
                path = path[idx + len('materials'):]
            qc_data.material_paths.append(path.strip('/\\'))
    
    # If no paths specified, use a default based on model name
    if not qc_data.material_paths and qc_data.model_name:
        qc_data.material_paths.append(f"models/{qc_data.model_name}")
    
    # Bodygroups
    qc_data.bodygroups = {}
    for box in qc_primary.bodygroup_boxes:
        enabled_collections = [
            item.name for item in box.collections if item.enabled
        ]
        if enabled_collections:
            qc_data.bodygroups[box.name] = enabled_collections
    
    # Sequences
    qc_data.sequences = []
    for rig_data in qc_primary.sequence_objectdata:
        for seq in rig_data.sequences:
            if seq.shouldExport:
                seq_dict = {
                    "name": seq.sequenceName or seq.originalName,
                    "file": seq.sequenceName or seq.originalName,
                    "fps": 30,  # Default FPS
                    "activity": getattr(seq, 'enum_activity', 'NONE'),
                    "activity_weight": 1
                }
                qc_data.sequences.append(seq_dict)
    
    # Character-specific settings
    qc_data.include_default_anims = toolbox.enum_qcGen_charAnimIncludes
    qc_data.definebones = toolbox.bool_qcGen_shouldDefineBones
    
    # Static prop flag for PROP and WORLDMODEL
    if qc_data.model_type in ("PROP", "WORLDMODEL"):
        qc_data.staticprop = True
    
    return qc_data


# ============================================================================
# Main QC Generation
# ============================================================================

def build_qc_content(qc_data: QCData) -> str:
    """
    Build the complete QC file content.
    
    Args:
        qc_data: QCData object with all model data
    
    Returns:
        Complete QC file content as string
    """
    # Load section order for this model type
    config = load_section_order(qc_data.model_type)
    sections = config.get("sections", [])
    flags = config.get("flags", [])
    
    lines = []
    
    # Header comment
    lines.append(f"// QC file generated by VonSourceTools")
    lines.append(f"// Model Type: {qc_data.model_type}")
    lines.append("")
    
    # Generate sections in order
    for section_name in sections:
        generator = SECTION_GENERATORS.get(section_name)
        if generator:
            content = generator(qc_data)
            if content:
                lines.append(content)
                lines.append("")
    
    # Generate flags
    for flag_name in flags:
        generator = FLAG_GENERATORS.get(flag_name)
        if generator:
            content = generator(qc_data)
            if content:
                lines.append(content)
                lines.append("")
    
    # Add definebones include if requested
    if qc_data.definebones:
        lines.append('$include "definebones.qci"')
        lines.append("")
    
    return "\n".join(lines)


def write_qc_file_from_data(qc_data: QCData) -> str:
    """
    Write a QC file from QCData.
    
    Args:
        qc_data: QCData object with all model data
    
    Returns:
        Path to the written file
    
    Raises:
        ValueError: If output path is not specified
    """
    if not qc_data.output_path:
        raise ValueError("No output path specified for QC file")
    
    # Build the QC content
    content = build_qc_content(qc_data)
    
    # Ensure output path has .qc extension
    output_path = qc_data.output_path
    if not output_path.lower().endswith('.qc'):
        output_path = output_path + '.qc'
    
    # Ensure directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # Write the file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return output_path


def generate_qc_file(context) -> str:
    """
    Main entry point: Generate a QC file from the current scene data.
    
    Args:
        context: Blender context
    
    Returns:
        Path to the generated QC file
    """
    # Gather all data from scene
    qc_data = gather_qc_data_from_scene(context)
    
    # Write the QC file
    return write_qc_file_from_data(qc_data)


# ============================================================================
# Legacy API (for backwards compatibility)
# ============================================================================

def get_all_vmt_filepaths() -> list:
    """
    Get all VMT file paths from the scene's QC_PrimaryData.
    
    Returns:
        list: List of VMT file path strings
    """
    if bpy is None:
        return []
    
    scene = bpy.context.scene
    qc_data = scene.QC_PrimaryData
    filepaths = [item.filepath for item in qc_data.vmt_filepaths if item.filepath]
    return filepaths


def gather_bodygroup_data() -> dict:
    """
    Collect bodygroup data from the scene's QC_PrimaryData.
    
    Returns:
        dict: Dictionary mapping bodygroup names to lists of enabled collection names.
    """
    if bpy is None:
        return {}
    
    qc_primary_data = bpy.context.scene.QC_PrimaryData
    bodygroups = {}
    
    for box in qc_primary_data.bodygroup_boxes:
        enabled_collections = [
            item.name
            for item in box.collections
            if item.enabled
        ]
        
        if enabled_collections:
            bodygroups[box.name] = enabled_collections
    
    return bodygroups


def gather_sequence_export_data(context) -> dict:
    """
    Gather sequence export data from the scene.
    
    Args:
        context: Blender context
    
    Returns:
        dict: Nested dictionary of sequence data
    """
    primary_data = context.scene.QC_PrimaryData
    export_data = {}
    
    def clean_enum(value):
        return "" if not value or value == "NONE" else value
    
    for rig in primary_data.sequence_objectdata:
        armature_name = rig.armatureName
        export_data[armature_name] = {}
        
        for seq in rig.sequences:
            original_name = seq.originalName or ""
            
            export_data[armature_name][original_name] = {
                "sequenceName": seq.sequenceName or "",
                "shouldExport": bool(seq.shouldExport),
                "qcPath": seq.qcPath or "",
                "customTag": seq.customTag or "",
                "activityCategory": clean_enum(
                    getattr(seq, "enum_activity_category", "")
                ),
                "activity": clean_enum(
                    getattr(seq, "enum_activity", "")
                )
            }
    
    return export_data


def get_sequences_dict(primary_data) -> dict:
    """
    Get a simplified dictionary of sequences per rig.
    
    Args:
        primary_data: The QC_PrimaryData property group
    
    Returns:
        dict: Format {RigName: [SequenceName, ...], ...}
    """
    if bpy is None:
        return {}
    
    sequences_dict = {}
    primary_data = bpy.context.scene.QC_PrimaryData
    
    for rig_data in primary_data.sequence_objectdata:
        rig_name = rig_data.armatureName
        sequence_names = [seq.sequenceName for seq in rig_data.sequences]
        sequences_dict[rig_name] = sequence_names
    
    return sequences_dict


def populate_template(template_file: str, replacements: dict) -> str:
    """
    Load a QC template and fill in placeholders.
    
    Args:
        template_file: Name of the template file (e.g., "modelname.txt")
        replacements: Dictionary of placeholder replacements
    
    Returns:
        str: The populated template content
    """
    template_content = load_template(template_file.replace('.txt', ''))
    return template_content.format_map(replacements)


def load_qc_section_order() -> dict:
    """
    Load the QC section order configuration.
    
    Returns:
        dict: The section order configuration for all model types
    """
    json_file = get_templates_directory() / "qc_section_order.json"
    
    if not json_file.exists():
        raise FileNotFoundError(f"QC section order JSON not found: {json_file}")
    
    with json_file.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_qc_file(qc_type: str, qc_commands: dict, qc_controls: dict) -> str:
    """
    Legacy API: Write a QC file based on the provided commands and controls.
    
    This function is kept for backwards compatibility.
    New code should use generate_qc_file() instead.
    
    Args:
        qc_type: Type of QC file (e.g., "npc", "prop", "character")
        qc_commands: Dictionary of QC commands and their values
        qc_controls: Dictionary of control settings (e.g., output path)
    
    Returns:
        Path to the written file
    """
    # Create a QCData object from the legacy parameters
    qc_data = QCData()
    qc_data.model_type = qc_type.upper()
    qc_data.model_name = qc_commands.get("modelname", "")
    qc_data.output_path = qc_controls.get("qc_output", "")
    qc_data.generate_collision = qc_commands.get("shouldGenCollis", False)
    qc_data.include_default_anims = qc_commands.get("includeanims", "None")
    
    # Gather additional data from scene if available
    if bpy is not None:
        qc_data.bodygroups = gather_bodygroup_data()
        qc_data.material_paths = get_all_vmt_filepaths()
    
    return write_qc_file_from_data(qc_data)
