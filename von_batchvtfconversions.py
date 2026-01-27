import subprocess # type: ignore
from pathlib import Path

def convert_file_with_structure(filePath: Path, exportFormat: str, inputFolder: Path, outputFolder: Path, vtfcmdExe: Path):
    relativePath = filePath.relative_to(inputFolder)
    outputSubfolder = outputFolder / relativePath.parent
    outputSubfolder.mkdir(parents=True, exist_ok=True)
    outputPath = outputSubfolder / (filePath.stem + f".{exportFormat}")

    cmd = [
        str(vtfcmdExe),
        "-file", str(filePath),
        "-output", str(outputSubfolder),
        "-exportformat", exportFormat,
        "-silent"
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Converted: {filePath} -> {outputPath}")
    except subprocess.CalledProcessError as e:
        print(f"Failed: {filePath}, {e}")


def batch_convert(context):
    scene = context.scene
    toolBox = scene.toolBox

    vtfcmdExe = Path(toolBox.string_vtfbatch_vtfccmdexe)
    inputFolder = Path(toolBox.string_vtfbatch_inputfolder)
    outputFolder = Path(toolBox.string_vtfbatch_outputfolder)
    sourceFiletype = toolBox.enum_vtfbatch_sourcefiletype
    targetFiletype = toolBox.enum_vtfbatch_targetfiletype

    if not inputFolder.exists():
        print(f"Input folder '{inputFolder}' does not exist.")
        return
    files = list(inputFolder.rglob(f"*.{sourceFiletype}"))
    if not files:
        print(f"No *.{sourceFiletype} files found in '{inputFolder}' folder.")
        return

    for file in files:
        convert_file_with_structure(file, targetFiletype, inputFolder, outputFolder, vtfcmdExe)

    print("Batch conversion completed!")
