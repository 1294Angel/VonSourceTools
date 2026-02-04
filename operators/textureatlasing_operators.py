import bpy # type: ignore
from ..utils.blender_utils import get_selected_meshes
from ..core.texture_atlas import *
from ..properties.texture_atlas_properties import *
logger = logging.getLogger(__name__)
get_pillow()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Image Packing
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


    
class von_panel_rig_checker_texture_atlas(bpy.types.Operator):
    bl_idname = "von.optimisationtools_textureatlasing"
    bl_label = "Texture Atlas"

    meshes: bpy.props.CollectionProperty(type=texture_atlas_mesh_item)

    def invoke(self, context, event):
        self.meshes.clear()
        selectedMeshes = get_selected_meshes(context)
        seenMaterials = set()
        for obj in selectedMeshes:
            meshItem = self.meshes.add()
            meshItem.meshName = obj.name
            for matSlot in obj.material_slots:
                if matSlot.material and matSlot.material.name not in seenMaterials:
                    seenMaterials.add(matSlot.material.name)
                    matItem = meshItem.materials.add()
                    matItem.name = matSlot.material.name

        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        seenMaterials = set()
        box = layout.box()
        box.label(text=("Select Materials To Atlas"))
        for meshItem in self.meshes:
            for matItem in meshItem.materials:
                if matItem.name not in seenMaterials:
                    seenMaterials.add(matItem.name)
                    row = box.row()
                    row.prop(matItem, "doWork", text="")
                    row.label(text=matItem.name)





    def execute(self, context):
        matObjDict = {}        
        matLinkDict = {}
        texturesBySocket = {}
        settings = context.scene.von_textureatlas_settings
        atlasSize = settings.atlas_size
        atlasOutputPath = settings.atlas_output_path
        shouldMoveUVs = settings.atlas_moveUVs



        for meshItem in self.meshes:
            obj = bpy.data.objects.get(meshItem.meshName)
            for matItem in meshItem.materials:
                if matItem.doWork == True:
                    matObjDict.setdefault(matItem.name, []).append(obj.name)
            
        matLinkDict = get_all_image_textures_from_discovered_materials(matObjDict)
        texturesBySocket = organise_textures_by_socket(matLinkDict)
        savedPaths, positions = pack_images(self, atlasOutputPath, texturesBySocket, atlasSize)
        if shouldMoveUVs:
            uvMapDict = convert_positions_to_uvs(positions, atlasSize)
            apply_uv_map_to_material_objects(matObjDict, uvMapDict)
        #Expand to include adding and moving materials to the relivant UV's - Maybe use seperate operator?
        return {'FINISHED'}
    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Hotspot texturing
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#To Do, same idea as: https://www.youtube.com/watch?v=qU7EjGv3iiE

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# For Registering
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

classes = [
    von_panel_rig_checker_texture_atlas
]


def register():
    from bpy.utils import register_class # type: ignore
    for cls in classes:
        register_class(cls)    

def unregister():
    from bpy.utils import unregister_class # type: ignore
    for cls in reversed(classes):
        unregister_class(cls)