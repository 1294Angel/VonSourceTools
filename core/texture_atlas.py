#==========================================================
#           Import libraries
#==========================================================
import bpy, os, sys, logging # type: ignore
from collections import defaultdict
from ..data.paths import get_pillow_path
#Setup Logger
logger = logging.getLogger(__name__)
#Import nessicary functions


def get_pillow():
    bundled_path = get_pillow_path()
    print(f"[DEBUG] Bundled path: {bundled_path}")
    print(f"[DEBUG] Path exists: {bundled_path.exists() if bundled_path else False}")
    
    if bundled_path and str(bundled_path) not in sys.path:
        sys.path.insert(0, str(bundled_path))
        print(f"[DEBUG] Added to sys.path: {bundled_path}")
    
    try:
        from PIL import Image
        print(f"[DEBUG] Pillow imported successfully (bundled)")
        return Image, True, "bundled" if bundled_path else "system"
    except ImportError as e:
        print(f"[DEBUG] Bundled import failed: {e}")
    
    try:
        from PIL import Image
        print(f"[DEBUG] Pillow imported successfully (system)")
        return Image, True, "system"
    except ImportError as e:
        print(f"[DEBUG] System import failed: {e}")
    
    return None, False, None

Image, PILLOW_AVAILABLE, PILLOW_SOURCE = get_pillow()
print(f"[DEBUG] Image: {Image}, Available: {PILLOW_AVAILABLE}, Source: {PILLOW_SOURCE}")
#==========================================================
#           Atlas Functions
#==========================================================

def get_all_selected_object_materials(selectedObjects):
    materialsFound = {}
    for obj in selectedObjects:
        if not obj.data or not hasattr(obj.data, "materials"):
            continue
        for mat in obj.data.materials:
            if mat:
                matName = mat.name
                if matName not in materialsFound:
                    materialsFound[matName] = []
                if obj.name not in materialsFound[matName]:
                    materialsFound[matName].append(obj.name)
    return materialsFound


def organise_textures_by_socket(matLinkDict):
    texturesBySocket = defaultdict(list)
    for matName, texList in matLinkDict.items():
        for texDict in texList:
            for socketName, imagePath in texDict.items():
                texturesBySocket[socketName].append((matName, imagePath))
    return texturesBySocket


def get_all_image_textures_from_discovered_materials(matObjDict):
    atlasMatLocations = {}
    for matName in matObjDict.keys():
        linksDict = {}
        mat = bpy.data.materials.get(matName)

        if not mat or not mat.use_nodes:
            continue
        for node in mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE' and node.image:
                for out in node.outputs:
                    for link in out.links:
                        linksDict[link.to_socket.name] = node.image.filepath
        atlasMatLocations[matName] = [linksDict]

    return atlasMatLocations


# ------------------------------------------------------------------------------
# Packing Into Atlas Sheets
# ------------------------------------------------------------------------------

def pack_images(self, atlasOutputPath, texturesBySocket, atlasSize=4096):
    if atlasSize % 2 != 0:
        atlasSize -= 1
    atlasesPaths = {}
    positions = {}

    for socket, tex_list in texturesBySocket.items():
        loaded_textures = []
        for matName, path in tex_list:
            abs_path = bpy.path.abspath(path)
            try:
                img = Image.open(abs_path).convert("RGBA")
                loaded_textures.append((matName, img))
            except Exception as e:
                logger.warning(f"Failed to load image {abs_path}: {e}")

        atlasIndex = 0
        x = 0
        y = 0
        rowHeight = 0

        atlas = Image.new("RGBA", (atlasSize, atlasSize), (0, 0, 0, 0))
        atlasesPaths.setdefault(socket, []).append(atlas)

        for matName, img in loaded_textures:
            w, h = img.size

            if x + w > atlasSize:
                x = 0
                y += rowHeight
                rowHeight = 0

            if y + h > atlasSize:
                atlasIndex += 1
                atlas = Image.new("RGBA", (atlasSize, atlasSize), (0, 0, 0, 0))
                atlasesPaths[socket].append(atlas)
                x = 0
                y = 0
                rowHeight = 0

            atlas.paste(img, (x, y))

            if matName not in positions:
                positions[matName] = {}
            positions[matName]["atlasIndex"] = (atlasIndex)
            positions[matName]["atlasFileLoc"] = os.path.join(bpy.path.abspath(atlasOutputPath),
                                                              f"{socket}_atlas_{atlasIndex}.png")
            positions[matName]["offset"] = (x, y, w, h)

            x += w
            rowHeight = max(rowHeight, h)

    savedPaths = {}
    for socket, atlasList in atlasesPaths.items():
        savedPaths[socket] = []
        for i, atlas in enumerate(atlasList):
            outputPath = os.path.join(bpy.path.abspath(atlasOutputPath), f"{socket}_atlas_{i}.png")
            atlas.save(outputPath)
            savedPaths[socket].append(outputPath)

    return savedPaths, positions


def convert_positions_to_uvs(positions, atlasSize):
    uvMap = {}
    for matName, data in positions.items():
        atlasIndex = data["atlasIndex"]
        atlasFileLoc = data["atlasFileLoc"]
        x, y, w, h = data["offset"]

        u_min = x / atlasSize
        u_max = (x + w) / atlasSize

        v_max = 1 - (y / atlasSize)
        v_min = 1 - ((y + h) / atlasSize)

        uvMap[matName] = {
            "atlasIndex": atlasIndex,
            "atlasFileLocation": atlasFileLoc,
            "uvRect": (u_min, v_min, u_max, v_max)
        }
    return uvMap


def apply_uv_map_to_material_objects(matObjDict, uvMap):
    for matName, objects in matObjDict.items():
        if matName not in uvMap:
            continue
        u_min, v_min, u_max, v_max = uvMap[matName]["uvRect"]
        u_scale = u_max - u_min
        v_scale = v_max - v_min

        for obj in objects:
            obj = bpy.data.objects.get(obj)
            mesh = obj.data
            if not mesh.uv_layers:
                continue
            uvLayer = mesh.uv_layers.active.data

            for poly in mesh.polygons:
                if obj.material_slots[poly.material_index].material.name != matName:
                    continue
                for loop_index in poly.loop_indices:
                    uv = uvLayer[loop_index].uv
                    uv[0] = u_min + uv[0] * u_scale
                    uv[1] = v_min + uv[1] * v_scale

            mesh.update()

def add_new_material(materialName:str, object):
     object.data.materials.append(bpy.data.materials[materialName])

def assign_imageTexture_to_material(materialName:str, object, imageTexturePaths):
    for imagePath in imageTexturePaths:
        print("")
        #finish



