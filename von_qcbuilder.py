import json, bpy # type: ignore
from pathlib import Path
from .von_common import load_json_dict_to_var

# ---------------------------------------------
# typical functions
# ---------------------------------------------
def get_all_vmt_filepaths()->list:
    scene = bpy.context.scene
    qc_data = scene.QC_PrimaryData
    filepaths = [item.filepath for item in qc_data.vmt_filepaths if item.filepath]
    return filepaths

def gather_bodygroup_data():
    qcPrimaryData = bpy.context.scene.QC_PrimaryData
    bodygroups = {}

    for box in qcPrimaryData.bodygroup_boxes:
        enabled_collections = [
            item.name
            for item in box.collections
            if item.enabled
        ]

        if enabled_collections:
            bodygroups[box.name] = enabled_collections

    return bodygroups # returns dict {"Bodygroup Name" : ["Collection Name""CollectioName" ect]}



def make_dictcommand_into_qccommand(inputCommand):
    outputcommand = f"${inputCommand}"
    return outputcommand

def populate_template(templateFile: str, replacements: dict) -> str:
    scriptDir  = Path(__file__).parent
    templatePath  = scriptDir  / "storeditems" / "qcgenerator" / "templates" / "commands" / templateFile

    with open(templatePath, "r", encoding="utf-8") as f:
        templateContent = f.read()

    populatedContent = templateContent.format_map(replacements)

    return populatedContent


def write_qc_file(qcType:str, qcCommands:dict, qcControls:dict):
    modelName:str = ""

    writeToQc = {}
    commandValidity = {}
    bodyGroups = gather_bodygroup_data()
    relativePath = "qcgenerator" / "templates"
    validCommandsOrder = load_json_dict_to_var(relativePath, "qc_section_order.json")

    for key in qcCommands.keys():
        if key in validCommandsOrder:
            commandValidity["True"].append(key)
        else:
            commandValidity["False"].append(key)
    for issue in commandValidity["False"]:
        print(f"ERROR Command: {issue} is not applicable to this type of qc.")
    qc = open(qcControls["qc_output"],"o")
    qc.close()

    #Qc Commands Add to QC file as needed
    for command in qcCommands.keys():
        if command == "modelname":
            populate_template(command, replacements={"mdlModelName":qcCommands[command]})
        elif command == "cdmaterials":
            #Go through each material folder given and create a new cdmaterials for each
            pass
        elif command == "include":
            pass
        elif command == "bodygroup":
            #go through each bodygroup and write studio "smd" for each of the selected smds in each bodygroup.
            pass
        elif command == "collisionmodel":
            pass
        elif command == "surfaceprop":
            pass
        elif command == "sequence":
            #Go through each NLA Track sequence on the selected armature and export seperately.
            pass
        elif command == "attachment":
            #loop through all attachment points based on the bone locations (NEEDS CROWBAR SUPPORT)
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
        
        
        
        




    

    

