import json, bpy # type: ignore
from pathlib import Path

# ---------------------------------------------
# dispatch functions
# ---------------------------------------------



# ---------------------------------------------
# typical functions
# ---------------------------------------------

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

def load_json_dict_to_var(relativePath: str, jsonFileName) -> dict:
    addonDir = Path(__file__).parent
    jsonPath = addonDir / relativePath / jsonFileName

    if not jsonPath.isfile():
        raise FileNotFoundError(f"Json Dict not found: {jsonPath}")
    with jsonPath.open("r", encoding="utf-8") as f:
        data = json.load(f)
    
    return data

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
        
        
        
        




    

    

