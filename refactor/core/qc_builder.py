"""
QC file generation logic.
"""
import json
import bpy  # type: ignore
from pathlib import Path

from ..data.paths import get_templates_directory, get_commands_directory
from ..utils.file_utils import load_json_data


def get_all_vmt_filepaths() -> list:
    """
    Get all VMT file paths from the scene's QC_PrimaryData.
    
    Returns:
        list: List of VMT file path strings
    """
    scene = bpy.context.scene
    qc_data = scene.QC_PrimaryData
    filepaths = [item.filepath for item in qc_data.vmt_filepaths if item.filepath]
    return filepaths


def gather_bodygroup_data() -> dict:
    """
    Collect bodygroup data from the scene's QC_PrimaryData.
    
    Returns:
        dict: Dictionary mapping bodygroup names to lists of enabled collection names.
              Format: {"BodygroupName": ["Collection1", "Collection2", ...]}
    """
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
        dict: Nested dictionary with format:
            {
                armatureName: {
                    originalSequenceName: {
                        sequenceName,
                        shouldExport,
                        qcPath,
                        customTag,
                        activityCategory,
                        activity
                    }
                }
            }
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
    sequences_dict = {}
    primary_data = bpy.context.scene.QC_PrimaryData
    
    for rig_data in primary_data.sequence_objectdata:
        rig_name = rig_data.armatureName
        sequence_names = [seq.sequenceName for seq in rig_data.sequences]
        sequences_dict[rig_name] = sequence_names
    
    return sequences_dict


def make_qc_command(command: str) -> str:
    """
    Convert a command name to QC format with $ prefix.
    
    Args:
        command: The command name
    
    Returns:
        str: The command with $ prefix
    """
    return f"${command}"


def populate_template(template_file: str, replacements: dict) -> str:
    """
    Load a QC template and fill in placeholders.
    
    Args:
        template_file: Name of the template file (e.g., "modelname.txt")
        replacements: Dictionary of placeholder replacements
    
    Returns:
        str: The populated template content
    """
    template_path = get_commands_directory() / template_file
    
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
    
    return template_content.format_map(replacements)


def load_qc_section_order() -> dict:
    """
    Load the QC section order configuration.
    
    Returns:
        dict: The section order configuration
    """
    json_file = get_templates_directory() / "qc_section_order.json"
    
    if not json_file.exists():
        raise FileNotFoundError(f"QC section order JSON not found: {json_file}")
    
    with json_file.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_qc_file(qc_type: str, qc_commands: dict, qc_controls: dict) -> None:
    """
    Write a QC file based on the provided commands and controls.
    
    Args:
        qc_type: Type of QC file (e.g., "npc", "prop", "character")
        qc_commands: Dictionary of QC commands and their values
        qc_controls: Dictionary of control settings (e.g., output path)
    """
    bodygroups = gather_bodygroup_data()
    valid_commands_order = load_qc_section_order()
    
    command_validity = {"True": [], "False": []}
    
    for key in qc_commands.keys():
        if key in valid_commands_order:
            command_validity["True"].append(key)
        else:
            command_validity["False"].append(key)
    
    for issue in command_validity["False"]:
        print(f"ERROR Command: {issue} is not applicable to this type of qc.")
    
    output_path = qc_controls.get("qc_output", "")
    if not output_path:
        raise ValueError("No output path specified")
    
    with open(output_path, "w", encoding="utf-8") as qc:
        # Write QC commands
        for command in qc_commands.keys():
            if command == "modelname":
                content = populate_template(
                    "modelname.txt",
                    {"mdlModelName": qc_commands[command]}
                )
                qc.write(content + "\n")
            elif command == "cdmaterials":
                # Handle material folders
                pass
            elif command == "include":
                pass
            elif command == "bodygroup":
                # Handle bodygroups
                pass
            elif command == "collisionmodel":
                pass
            elif command == "surfaceprop":
                pass
            elif command == "sequence":
                # Handle sequences
                pass
            elif command == "attachment":
                pass
            elif command == "hboxset":
                pass
            elif command == "illumposition":
                pass
            elif command == "origin":
                pass
            elif command == "includemodel":
                pass
            elif command == "staticprop":
                pass
