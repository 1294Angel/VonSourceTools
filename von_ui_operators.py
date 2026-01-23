import json, bpy, bmesh, os, subprocess # type: ignore
from mathutils import Vector # type: ignore
from pathlib import Path # type: ignore
from . import von_deltaanimtrick
from . import von_common
from . import von_qcbuilder
from .von_batchvtfconversions import batch_convert
#-------------------------------------------------------------------------------------------------------------------------------------------------
# Delta Anim Trick
#-------------------------------------------------

def has_properties():
    print("-----------------------Running Has_Properties -----------------------")
    hasProportions = bpy.data.objects.get("proportions")
    hasMaleRef = bpy.data.objects.get("reference_female")
    hasFemaleRef = bpy.data.objects.get("reference_male")

    if hasProportions:
        for col in hasProportions.users_collection:
            col.objects.unlink(hasProportions)
        bpy.data.objects.remove(hasProportions)
        von_common.importitemfromdict("proportions", "Collection 2", von_common.deltaanimtrick_armaturefilelocations())
        hasProportions = True
    else:
        von_common.importitemfromdict("proportions", "Collection 2", von_common.deltaanimtrick_armaturefilelocations())
        hasProportions = True
    if not hasFemaleRef:
        von_common.importitemfromdict("reference_female", "Collection 3", von_common.deltaanimtrick_armaturefilelocations())
        hasFemaleRef = True
    else:
        hasFemaleRef = True
    if not hasMaleRef:
        von_common.importitemfromdict("reference_male", "Collection 3", von_common.deltaanimtrick_armaturefilelocations())
        hasMaleRef = True
    else:
        hasMaleRef = True

    print(hasProportions, hasMaleRef, hasFemaleRef)
    bpy.data.objects.get("proportions").select_set(False)
    return hasProportions, hasMaleRef, hasFemaleRef

def is_valve_biped(armature, context):
    print("----------------------- Running Is_Valve_Biped -----------------------")
    scene = context.scene
    toolBox = scene.toolBox

    itteration:float = 0
    simmilarityThreshold:float = 0

    armatureBones = armature.data.bones
    simmilarityThreshold = toolBox.float_deltaAnim_simmilarityThreshold

    for bone in armatureBones:
        if bone.name in von_common.deltaanimtrick_valvebipeds_1():
            if "_end" in bone.name:
                pass
            else:
                itteration += 1.0
    
    matchingPercentage = itteration / float(len(armatureBones))
    matchingPercentage = matchingPercentage * 100

    if matchingPercentage >= simmilarityThreshold:
        return True
    else:
        return False
            
class Vonpanel_DeltaAnimTrick_ImportRequiredProperties(bpy.types.Operator):
    bl_idname = "von.deltaanimtrick_importrequiredproperties"
    bl_label = "Import Required Armatures"
    def execute(self,context):
        print("-----------------------Running Import Required Properties -----------------------")
        hasProportions, hasMaleRef, hasFemaleRef = has_properties()
        try:
            print(f"hasProportions = {hasProportions} ||| hasMaleRef = {hasMaleRef} ||| hasFemaleRef = {hasFemaleRef}")
        except:
            return{'CANCELLED'}
        return{'FINISHED'}

class VonPanel_DeltaAnimTrick_PartOne(bpy.types.Operator):
    bl_idname = "von.deltaanimtrick_partone"
    bl_label = "Delta Anim Trick (One)"
    def execute(self, context):
        print("-----------------------Running Delta Anim Trick 1 -----------------------")
        #Import reference armatures
        hasProportions: bool = False
        hasMaleRef: bool = False
        hasFemaleRef: bool = False

        hasProportions, hasMaleRef, hasFemaleRef = has_properties()

        if hasProportions and hasMaleRef and hasFemaleRef:
            #Get selected armatures
            obj = [obj for obj in bpy.data.objects if obj.type == "ARMATURE"]
            #Run once on each valid armature
            for armature in obj:
                von_deltaanimtrick.delta_anim_trick_one(armature)
            return{"FINISHED"}
        return{'CANCELLED'}

class VonPanel_DeltaAnimTrick_PartTwo(bpy.types.Operator):
    bl_idname = "von.deltaanimtrick_parttwo"
    bl_label = "Delta Anim Trick (Two)"
    def execute(self, context):
        print("-----------------------Running Delta Anim Trick 2 -----------------------")
        #Import reference armatures
        hasProportions: bool = False
        hasMaleRef: bool = False
        hasFemaleRef: bool = False
        hasProportions, hasMaleRef, hasFemaleRef = has_properties()

        if hasProportions and hasMaleRef and hasFemaleRef:
            #Get selected armatures
            obj = [obj for obj in bpy.data.objects if obj.type == "ARMATURE"]
            #Run once on each valid armature
            for armature in obj:
                von_deltaanimtrick.delta_anim_trick_two(armature.name)
            return{"FINISHED"}
        return{'CANCELLED'}

class VonPanel_DeltaAnimTrick_Full(bpy.types.Operator):
    bl_idname = "von.deltaanimtrick_full"
    bl_label = "Delta Anim Trick (Full)"
        

    def execute(self, context):
        print("-----------------------Running Delta Anim Trick FULL -----------------------")
        scene = context.scene
        toolBox = scene.toolBox

        failures:list = []
        hasvalvepiedarmature:bool = True

        obj = [obj for obj in bpy.context.selected_objects if obj.type == "ARMATURE"]
        firstobj = obj[0]
        if not obj:
            self.report({'ERROR'}, f"No Armature Detected")
            return{'CANCELLED'}

        for armature in obj:
            if is_valve_biped(armature, context):
                pass
            else:
                hasvalvepiedarmature = False
                failures.append(armature)
        if hasvalvepiedarmature == False:
            for failure in failures:
                self.report({'ERROR'}, f"{failure.name} has failed to meet the current simmilarity threshold of {toolBox.float_deltaAnim_simmilarityThreshold} | Please either lower threshold or ensure the armature uses valve biped armature on core deformation bones.")
            return{'CANCELLED'}
        
        firstobj.select_set(True)

        

        print("Checkpoint 1")
        #Import reference armatures
        hasProportions: bool = False
        hasMaleRef: bool = False
        hasFemaleRef: bool = False
        hasProportions, hasMaleRef, hasFemaleRef = has_properties()
        von_common.reselect_all(obj, obj[0])

        if hasProportions and hasMaleRef and hasFemaleRef:
            for armatureDataBlock in obj:
                print(armatureDataBlock)
                bpy.context.view_layer.objects.active = obj[0]

                print("Checkpoint 2")
                bpy.ops.object.mode_set(mode='EDIT')
                editbones = armatureDataBlock.data.edit_bones
                bpy.ops.object.mode_set(mode='POSE')

                armatureobject = bpy.data.objects[armatureDataBlock.name]
                posebones = armatureobject.pose.bones

                von_deltaanimtrick.delta_anim_trick_one(armatureDataBlock)



                #NEEDS TO ONLY AFFECT PROPORTIONS BONES
                proportionsArmature = bpy.data.objects["proportions"]
                bpy.context.view_layer.objects.active = proportionsArmature
                bpy.ops.object.mode_set(mode='EDIT')
                proportionsEditBones = proportionsArmature.data.edit_bones
                for bone in proportionsEditBones:
                    if bone.name == "ValveBiped.Bip01_L_Toe0" or bone.name == "ValveBiped.Bip01_L_Toe0":
                        von_deltaanimtrick.toevertical(bone)
            
                
                

                bpy.context.view_layer.objects.active = proportionsArmature
                bpy.ops.object.mode_set(mode='POSE')
                proportionsPoseBones = proportionsArmature.pose.bones
                bpy.ops.pose.armature_apply(selected=False)
                for bone in proportionsPoseBones:
                    von_deltaanimtrick.clearposeboneconstraints(bone, proportionsArmature)
                
                von_deltaanimtrick.delta_anim_trick_two(armature.name)
            bpy.context.view_layer.objects.active = proportionsArmature
            bpy.ops.object.mode_set(mode='OBJECT')
            self.report({'INFO'}, "Delta Anim Trick Successful | Test in HLMV and use advanced process if unsucessful")
            return{"FINISHED"}
        return{'CANCELLED'}

#-------------------------------------------------------------------------------------------------------------------------------------------------
# QC Generator Script
#-------------------------------------------------
def get_qc_templates_dir() -> Path:
    addon_dir = Path(__file__).parent
    return addon_dir / "qcgenerator" / "templates"

def load_qc_section_order() -> dict:
    templates_dir = get_qc_templates_dir()
    json_file = templates_dir / "qc_section_order.json"

    if not json_file.exists():
        raise FileNotFoundError(f"QC section order JSON not found: {json_file}")

    with json_file.open("r", encoding="utf-8") as f:
        return json.load(f)

def load_qc_template(template_name: str) -> str:
    templates_dir = get_qc_templates_dir() / "commands"
    template_file = templates_dir / f"{template_name}.txt"

    if not template_file.exists():
        raise FileNotFoundError(f"QC template not found: {template_file}")

    return template_file.read_text(encoding="utf-8")



#-- generate Collis
def get_skinned_meshes(armature):
    controlled_meshes = []
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            for mod in obj.modifiers:
                if mod.type == 'ARMATURE' and mod.object == armature:
                    controlled_meshes.append(obj)
                    break
    return controlled_meshes

def getallvertices_highest_vertexgroups_and_vert_location(ob):
    me = ob.data
    vertexgroups = ob.vertex_groups
    vgroups:dict = {}
    index_to_name = {vg.index: vg.name for vg in vertexgroups}   
    for vg in vertexgroups:
        vgroups[vg.name] = []
    for v in me.vertices:
        if not v.groups:
            continue
        highestInfluence = max(v.groups, key=lambda g: g.weight)
        group_name = index_to_name[highestInfluence.group]
        world_co = ob.matrix_world @ v.co.copy()
        vgroups[group_name].append(world_co)
    for key, data in vgroups.items():
        print(key)
        for vector in data:
            print(vector)
    return vgroups

def generate_collission_model_data(dictHighestVertexGroupPerVert:dict, obj):
    dict_collission_bounds:dict = {}
    for vGroup, data in dictHighestVertexGroupPerVert.items():
        if not data:
            continue
        xCords = []
        yCords = []
        zCords = []
        for v in data:
            world_co = obj.matrix_world @ v
            xCords.append(world_co.x)
            yCords.append(world_co.y)
            zCords.append(world_co.z)

        minX, maxX = min(xCords), max(xCords)
        minY, maxY = min(yCords), max(yCords)
        minZ, maxZ = min(zCords), max(zCords)
        
        corners = {
            "0_bottom_back_right"  : (maxX, minY, minZ),
            "1_bottom_front_right" : (maxX, maxY, minZ),
            "2_bottom_front_left"  : (minX, maxY, minZ),
            "3_bottom_back_left"   : (minX, minY, minZ),
            "4_top_back_right"     : (maxX, minY, maxZ),
            "5_top_front_right"    : (maxX, maxY, maxZ),
            "6_top_front_left"     : (minX, maxY, maxZ),
            "7_top_back_left"      : (minX, minY, maxZ),
        }

        dict_collission_bounds[vGroup] = corners
    return dict_collission_bounds

def create_collision_boxes_correct(dict_collision_bounds:dict, collection_name:str="collisions", wireframe:bool=False, prefix:str = "CollisionCube"):
    for vGroup, corners in dict_collision_bounds.items():
        print(vGroup)
        for vertexpos, vector in corners.items():
            print(vertexpos)
            print(vector)


    collisions_col = bpy.data.collections.get(collection_name)
    if collisions_col is None:
        collisions_col = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(collisions_col)

    created_objs = []

    for vGroup, corners in dict_collision_bounds.items():
        verts_coords = [
            corners["0_bottom_back_right"],  # 0
            corners["1_bottom_front_right"],  # 1
            corners["2_bottom_front_left"],  # 2
            corners["3_bottom_back_left"],  # 3
            corners["4_top_back_right"],  # 4
            corners["5_top_front_right"],  # 5
            corners["6_top_front_left"],  # 6
            corners["7_top_back_left"],  # 7
        ]

        face_indices = [
            (0, 1, 2, 3),
            (4, 5, 6, 7),
            (0, 4, 5, 1),
            (1, 5, 6, 2),
            (2, 6, 7, 3),
            (3, 7, 4, 0)
        ]

        mesh = bpy.data.meshes.new(f"collision_cube_{vGroup}")
        bm = bmesh.new()
        bm_verts = [bm.verts.new(co) for co in verts_coords]
        bm.verts.ensure_lookup_table()

        for fi in face_indices:
            face = bm.faces.new([bm_verts[i] for i in fi])
            face.smooth = True
        bm.to_mesh(mesh)
        bm.free()

        obj = bpy.data.objects.new(f"{prefix}_{vGroup}", mesh)
        collisions_col.objects.link(obj)

        if wireframe:
            obj.display_type = 'WIRE'
            try:
                obj.color = (0.0, 1.0, 0.0, 0.25)
            except Exception:
                pass

        created_objs.append(obj)

    return created_objs

def parent_collision_cubes_to_bones(armature_obj, prefix="CollisionCube_"):
    if armature_obj.type != 'ARMATURE':
        print(f"{armature_obj.name} is not an armature object.")
        return

    bpy.ops.object.mode_set(mode='OBJECT')

    for obj in bpy.data.objects:
        if not obj.name.startswith(prefix):
            continue

        bone_name = obj.name[len(prefix):]

        if bone_name not in armature_obj.data.bones:
            print(f"Bone '{bone_name}' not found for object '{obj.name}'")
            continue

        obj.parent = armature_obj
        obj.parent_type = 'BONE'
        obj.parent_bone = bone_name

        obj.matrix_parent_inverse = armature_obj.matrix_world.inverted()

        print(f"Parented '{obj.name}' → bone '{bone_name}'")

    print("Parenting complete.")

def create_collission_boxes(armaturelist):
    for armature in armaturelist:
            skinnedMeshes = get_skinned_meshes(armature)
            for mesh in skinnedMeshes:
                highestGroups = getallvertices_highest_vertexgroups_and_vert_location(mesh)
                collisionBounds = generate_collission_model_data(highestGroups, mesh)
                create_collision_boxes_correct(collisionBounds)
                parent_collision_cubes_to_bones(armature)

#-- get Sequences
def collect_actions_from_armature(obj):
    actions = set()
    ad = obj.animation_data
    if not ad:
        return actions
    if ad.action:
        actions.add(ad.action)
    for track in ad.nla_tracks:
        for strip in track.strips:
            if strip.action:
                actions.add(strip.action)
    return actions
class QC_OT_collect_sequences(bpy.types.Operator):
    bl_idname = "von.collect_sequences"
    bl_label = "Collect Animation Sequences"

    def execute(self, context):
        primaryData = context.scene.QC_PrimaryData
        primaryData.sequence_objectdata.clear()

        for obj in context.selected_objects:
            if obj.type != 'ARMATURE':
                continue

            rigData = primaryData.sequence_objectdata.add()
            rigData.armatureName = obj.name

            actions = collect_actions_from_armature(obj)

            for action in actions:
                seq = rigData.sequences.add()
                seq.sequenceName = action.name

        return {'FINISHED'}

#-- studiomdl definebones

def run_definebones_from_vondata(context):
    scene = context.scene
    toolBox = scene.toolBox
    studiomdlExe = Path(toolBox.string_studiomdl_filelocation).resolve()
    qcPath = Path(toolBox.string_qcGen_outputPath).resolve()
    gmodExe = Path(toolBox.string_gmodexe_path).resolve()
    verbose = toolBox.bool_studiomdl_verbose

    if not studiomdlExe.exists():
        raise FileNotFoundError(f"studiomdl.exe not found at {studiomdlExe}")
    if not qcPath.exists():
        raise FileNotFoundError(f"QC file not found at {qcPath}")
    if not gmodExe.exists():
        raise FileNotFoundError(f"Gmod.exe not found at {gmodExe}")
    gmodFolder = gmodExe.parent

    command = [
        str(studiomdlExe),
        "-definebones",
        "-verbose",
        "-game", str(gmodFolder),
        str(qcPath)
    ]
    result = subprocess.run(
        command,
        cwd=studiomdlExe.parent,
        capture_output=True,
        text=True
    )

    if verbose:
        print("=== STDOUT ===")
        print(result.stdout)
        print("=== STDERR ===")
        print(result.stderr)

    return result.stdout, result.stderr

class OBJECT_OT_run_definebones_vondata(bpy.types.Operator):
    bl_idname = "von.run_definebones_vondata"
    bl_label = "Run Define Bones"

    def execute(self, context):
        scene = context.scene
        toolBox = scene.toolBox

        try:
            stdout, stderr = run_definebones_from_vondata(context)
            self.report({'INFO'}, "Define Bones completed. Check console for output.")
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        return {'FINISHED'}

class Vonpanel_qcgenerator_player(bpy.types.Operator):
    bl_idname = "von.qcgenerator_player"
    bl_label = "Generate QC File"
    def execute(self,context):
        scene = context.scene
        toolBox = scene.toolBox
        flags = []
        sections = []
        modelname = toolBox.string_qcGen_mdlModelName
        qc_output = toolBox.string_qcGen_outputPath
        shouldGenCollis = toolBox.bool_qcGen_generateCollission
        selectedArmatures = [armature for armature in bpy.context.selected_objects if armature.type == "ARMATURE"]

        if shouldGenCollis:
            create_collission_boxes(selectedArmatures)
        if not shouldGenCollis:
            collisioncollection = toolBox.string_qcGen_existingCollissionCollection


        
        


        


            
            




        return{'FINISHED'}
class Vonpanel_qcgenerator_npc(bpy.types.Operator):
    bl_idname = "von.qcgenerator_npc"
    bl_label = "Generate QC File"
    def execute(self,context):
        qcCommands = {}
        qcControls = {}
        scene = context.scene
        toolBox = scene.toolBox
        qcCommands = {
            "modelname" : toolBox.string_qcGen_mdlModelName,
            "shouldGenCollis" : toolBox.bool_qcGen_generateCollission,
            "includeanims" : toolBox.enum_qcGen_charAnimIncludes
        }
        qcControls = {
            "qc_output" : toolBox.string_qcGen_outputPath
        }

        von_qcbuilder.write_qc_file("npc", qcCommands, qcControls)

        return{'FINISHED'}
class Vonpanel_RefreshCollections(bpy.types.Operator):
    bl_idname = "von.qcgenerator_refresh_collections"
    bl_label = "Refresh Collection List"

    def execute(self, context):
        scene = context.scene
        von_common.sync_bodygroup_boxes(scene)
        self.report({'INFO'}, "Collections synced with scene.")
        return {'FINISHED'}
        
def split_objects_into_collections(context):
    """Split all objects into temporary collections named original_objectname."""
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

def restore_objects_from_collections(context):
    mapping = context.scene.get('_collection_split_mapping')
    if not mapping:
        print("No mapping found. Nothing to restore.")
        return

    for obj_name, data in mapping.items():
        obj = context.scene.objects.get(obj_name)
        if not obj:
            continue

        for new_col_name in data['new']:
            new_col = bpy.data.collections.get(new_col_name)
            if new_col and obj.name in new_col.objects:
                new_col.objects.unlink(obj)
                if len(new_col.objects) == 0:
                    bpy.data.collections.remove(new_col)

        for orig_col_name in data['original']:
            orig_col = bpy.data.collections.get(orig_col_name)
            if orig_col and obj.name not in orig_col.objects:
                orig_col.objects.link(obj)
            elif not orig_col:
                if obj.name not in context.scene.collection.objects:
                    context.scene.collection.objects.link(obj)

    del context.scene['_collection_split_mapping']
class OBJECT_OT_split_objects(bpy.types.Operator):
    bl_idname = "object.split_objects"
    bl_label = "Split Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        split_objects_into_collections(context)
        self.report({'INFO'}, "Objects split into temporary collections.")
        return {'FINISHED'}

class OBJECT_OT_restore_objects(bpy.types.Operator):
    bl_idname = "object.restore_objects"
    bl_label = "Restore Objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        restore_objects_from_collections(context)
        self.report({'INFO'}, "Objects restored to original collections.")
        return {'FINISHED'}

class OBJECT_OT_export_smd(bpy.types.Operator):
    bl_idname = "object.export_smd"
    bl_label = "Export Scene"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        scene = context.scene
        toolBox = scene.toolBox
        export_folder = toolBox.string_export_folder
        for obj in context.scene.objects:
            obj.select_set(True)

        if not os.path.exists(self.string_export_folder):
            os.makedirs(self.string_export_folder)

        try:
            bpy.ops.export_scene.smd('INVOKE_DEFAULT')
        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {e}")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Export started. Choose folder in the popup.")
        return {'FINISHED'}


#Batch Convert Images
class Vonpanel_batchconvert_imagefiles(bpy.types.Operator):
    bl_idname = "von.batchconvertfiletypes"
    bl_label = "Convert Filetypes"

    def execute(self, context):
        scene = context.scene
        toolBox = scene.toolBox
        batch_convert(context)
        return {'FINISHED'}
# ----------------------------------------------------------------------------------------------------------------------------------------------------
# Register Fnction
# ----------------------------


classes = (
    #Delta Anim
    Vonpanel_DeltaAnimTrick_ImportRequiredProperties,
    VonPanel_DeltaAnimTrick_PartOne,
    VonPanel_DeltaAnimTrick_PartTwo,
    VonPanel_DeltaAnimTrick_Full,
    #QC Gen
    QC_OT_collect_sequences,
    Vonpanel_qcgenerator_player,
    Vonpanel_qcgenerator_npc,
    Vonpanel_RefreshCollections,
    OBJECT_OT_run_definebones_vondata,
    #Batch Smd Exporter
    OBJECT_OT_split_objects,
    OBJECT_OT_restore_objects,
    OBJECT_OT_export_smd,

    #Batch Image Filetype Changer
    Vonpanel_batchconvert_imagefiles,
)


def von_operator_register():
    for cls in classes:
        bpy.utils.register_class(cls)    


def von_operator_unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)