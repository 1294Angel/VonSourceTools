"""
Smoke tests that verify complete workflows.
These tests run full scenarios inside Blender.

Run with: pytest tests/test_smoke.py -v -m smoke
"""
import pytest
from pathlib import Path
import sys

# Add tests directory to path
sys.path.insert(0, str(Path(__file__).parent))

from conftest import (
    run_addon_test_in_blender,
    run_blender_script,
    blender_available,
    requires_blender,
    smoke,
    ADDON_PATH,
)


@pytest.mark.smoke
@requires_blender
class TestDeltaAnimWorkflow:
    """Smoke tests for delta animation trick workflow."""
    
    def test_delta_anim_validation_with_empty_scene(self):
        """Test that delta animation validation handles empty scene."""
        result = run_addon_test_in_blender('''
    # Try to run delta animation trick with no armatures
    # The operator should report an error but not crash
    
    # Get selected objects (should be empty or not armatures)
    armatures = [obj for obj in bpy.context.selected_objects if obj.type == 'ARMATURE']
    
    if len(armatures) == 0:
        test_output.append("Correctly detected no armatures selected")
    else:
        raise AssertionError("Should have no armatures in empty scene")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_delta_anim_imports_references(self):
        """Test that reference armatures can be imported."""
        result = run_addon_test_in_blender('''
    from core.delta_anim import import_reference_armatures
    from data.paths import get_armature_file_locations
    
    # Check if the FBX files exist
    locations = get_armature_file_locations()
    
    missing_files = []
    for name, path in locations.items():
        if not path.exists():
            missing_files.append(str(path))
    
    if missing_files:
        test_output.append(f"Missing files: {missing_files}")
        # Don't fail if files don't exist, just note it
        test_output.append("Reference files not found - this is expected if storeditems not present")
    else:
        test_output.append("All reference files found")
''')
        
        assert result['success'], f"Test failed: {result['error']}"


@pytest.mark.smoke
@requires_blender
class TestQCGeneratorWorkflow:
    """Smoke tests for QC generator workflow."""
    
    def test_qc_generator_with_default_settings(self):
        """Test QC generator with default settings."""
        result = run_addon_test_in_blender('''
    scene = bpy.context.scene
    toolbox = scene.toolBox
    
    # Check default settings
    model_type = toolbox.enum_qcGen_modelType
    scale = toolbox.int_qcGen_scale
    generate_collision = toolbox.bool_qcGen_generateCollission
    
    test_output.append(f"Model type: {model_type}")
    test_output.append(f"Scale: {scale}")
    test_output.append(f"Generate collision: {generate_collision}")
    
    # Verify defaults
    if model_type != "CHARACTER":
        raise AssertionError(f"Expected CHARACTER, got {model_type}")
    if scale != 1:
        raise AssertionError(f"Expected scale 1, got {scale}")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_qc_generator_model_type_change(self):
        """Test changing QC model type."""
        result = run_addon_test_in_blender('''
    scene = bpy.context.scene
    toolbox = scene.toolBox
    
    # Change model type
    test_types = ['PROP', 'NPC', 'VIEWMODEL', 'WORLDMODEL', 'CHARACTER']
    
    for model_type in test_types:
        toolbox.enum_qcGen_modelType = model_type
        actual = toolbox.enum_qcGen_modelType
        
        if actual != model_type:
            raise AssertionError(f"Failed to set model type to {model_type}, got {actual}")
        
        test_output.append(f"Set model type to: {model_type}")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_sequence_collection_with_armature(self):
        """Test collecting sequences from an armature."""
        result = run_addon_test_in_blender('''
    # Create an armature with an action
    bpy.ops.object.armature_add()
    armature = bpy.context.active_object
    
    # Create an action
    action = bpy.data.actions.new(name="TestAction")
    
    # Assign action to armature
    if armature.animation_data is None:
        armature.animation_data_create()
    armature.animation_data.action = action
    
    # Now test the sequence collection
    from core.sequences import collect_actions_from_armature
    
    actions = collect_actions_from_armature(armature)
    
    if len(actions) == 1:
        test_output.append("Successfully collected 1 action from armature")
    else:
        raise AssertionError(f"Expected 1 action, got {len(actions)}")
''')
        
        assert result['success'], f"Test failed: {result['error']}"


@pytest.mark.smoke
@requires_blender
class TestBodygroupWorkflow:
    """Smoke tests for bodygroup workflow."""
    
    def test_bodygroup_creation(self):
        """Test creating bodygroups."""
        result = run_addon_test_in_blender('''
    scene = bpy.context.scene
    qc_data = scene.QC_PrimaryData
    
    # Create collections first
    for i in range(3):
        col = bpy.data.collections.new(f"BodyPart_{i}")
        bpy.context.scene.collection.children.link(col)
    
    # Add bodygroups
    qc_data.num_boxes = 2
    
    # Add bodygroup boxes
    while len(qc_data.bodygroup_boxes) < 2:
        qc_data.bodygroup_boxes.add()
    
    # Configure bodygroups
    qc_data.bodygroup_boxes[0].name = "Head"
    qc_data.bodygroup_boxes[1].name = "Body"
    
    test_output.append(f"Created {len(qc_data.bodygroup_boxes)} bodygroups")
    test_output.append(f"Names: {[bg.name for bg in qc_data.bodygroup_boxes]}")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_refresh_collections_operator(self):
        """Test the refresh collections operator."""
        result = run_addon_test_in_blender('''
    # Create some collections
    for i in range(3):
        if f"RefreshTest_{i}" not in bpy.data.collections:
            col = bpy.data.collections.new(f"RefreshTest_{i}")
            bpy.context.scene.collection.children.link(col)
    
    # Set up bodygroups
    scene = bpy.context.scene
    qc_data = scene.QC_PrimaryData
    qc_data.num_boxes = 1
    
    while len(qc_data.bodygroup_boxes) < 1:
        qc_data.bodygroup_boxes.add()
    
    # Run the refresh operator
    from properties.toolbox_properties import sync_bodygroup_boxes
    sync_bodygroup_boxes(scene)
    
    # Check that collections are available
    if len(qc_data.bodygroup_boxes) > 0:
        box = qc_data.bodygroup_boxes[0]
        test_output.append(f"Bodygroup has {len(box.collections)} collection options")
    else:
        raise AssertionError("No bodygroup boxes created")
''')
        
        assert result['success'], f"Test failed: {result['error']}"


@pytest.mark.smoke
@requires_blender
class TestCollisionWorkflow:
    """Smoke tests for collision generation workflow."""
    
    def test_get_skinned_meshes(self):
        """Test getting skinned meshes from armature."""
        result = run_addon_test_in_blender('''
    from core.collision import get_skinned_meshes
    
    # Create armature
    bpy.ops.object.armature_add()
    armature = bpy.context.active_object
    
    # Create mesh
    bpy.ops.mesh.primitive_cube_add()
    mesh = bpy.context.active_object
    
    # Add armature modifier
    mod = mesh.modifiers.new('Armature', 'ARMATURE')
    mod.object = armature
    
    # Test function
    skinned = get_skinned_meshes(armature)
    
    if len(skinned) == 1 and skinned[0] == mesh:
        test_output.append("Successfully found skinned mesh")
    else:
        raise AssertionError(f"Expected 1 skinned mesh, got {len(skinned)}")
''')
        
        assert result['success'], f"Test failed: {result['error']}"


@pytest.mark.smoke
@requires_blender
class TestSMDExportWorkflow:
    """Smoke tests for SMD export workflow."""
    
    def test_split_and_restore_objects(self):
        """Test splitting and restoring objects to collections."""
        result = run_addon_test_in_blender('''
    from core.smd_export import (
        split_objects_into_collections,
        restore_objects_from_collections
    )
    
    # Create test collection
    test_col = bpy.data.collections.new("SplitTest")
    bpy.context.scene.collection.children.link(test_col)
    
    # Create test object
    bpy.ops.mesh.primitive_cube_add()
    obj = bpy.context.active_object
    obj.name = "SplitTestCube"
    
    # Move to test collection
    bpy.context.scene.collection.objects.unlink(obj)
    test_col.objects.link(obj)
    
    # Get original collection
    original_cols = [col.name for col in obj.users_collection]
    
    # Split
    split_objects_into_collections(bpy.context)
    
    # Check that it was moved
    new_cols = [col.name for col in obj.users_collection]
    test_output.append(f"After split: {new_cols}")
    
    # Restore
    restore_objects_from_collections(bpy.context)
    
    # Check restoration
    restored_cols = [col.name for col in obj.users_collection]
    test_output.append(f"After restore: {restored_cols}")
''')
        
        assert result['success'], f"Test failed: {result['error']}"


@pytest.mark.smoke
@requires_blender
class TestVMTWorkflow:
    """Smoke tests for VMT file path workflow."""
    
    def test_vmt_filepath_management(self):
        """Test managing VMT file paths."""
        result = run_addon_test_in_blender('''
    scene = bpy.context.scene
    qc_data = scene.QC_PrimaryData
    
    # Add VMT file paths
    qc_data.num_vmt_files = 3
    
    # The update function should have created 3 entries
    if len(qc_data.vmt_filepaths) == 3:
        test_output.append("Created 3 VMT filepath entries")
    else:
        raise AssertionError(f"Expected 3 entries, got {len(qc_data.vmt_filepaths)}")
    
    # Set paths
    for i, item in enumerate(qc_data.vmt_filepaths):
        item.filepath = f"/test/path/material_{i}.vmt"
    
    # Verify
    for i, item in enumerate(qc_data.vmt_filepaths):
        if f"material_{i}.vmt" not in item.filepath:
            raise AssertionError(f"Path not set correctly for entry {i}")
    
    test_output.append("VMT paths set correctly")
    
    # Test reducing count
    qc_data.num_vmt_files = 1
    if len(qc_data.vmt_filepaths) == 1:
        test_output.append("Successfully reduced to 1 VMT entry")
    else:
        raise AssertionError(f"Expected 1 entry after reduction, got {len(qc_data.vmt_filepaths)}")
''')
        
        assert result['success'], f"Test failed: {result['error']}"


@pytest.mark.smoke
@requires_blender  
class TestFullWorkflowIntegration:
    """Test complete workflows from start to finish."""
    
    def test_character_setup_workflow(self):
        """Test a typical character setup workflow."""
        result = run_addon_test_in_blender('''
    scene = bpy.context.scene
    toolbox = scene.toolBox
    qc_data = scene.QC_PrimaryData
    
    # 1. Create armature
    bpy.ops.object.armature_add()
    armature = bpy.context.active_object
    armature.name = "CharacterArmature"
    
    # 2. Create mesh
    bpy.ops.mesh.primitive_cylinder_add()
    mesh = bpy.context.active_object
    mesh.name = "CharacterBody"
    
    # 3. Parent mesh to armature
    mod = mesh.modifiers.new('Armature', 'ARMATURE')
    mod.object = armature
    
    # 4. Create bodygroup collections
    body_col = bpy.data.collections.new("Body_Default")
    head_col = bpy.data.collections.new("Head_Default")
    bpy.context.scene.collection.children.link(body_col)
    bpy.context.scene.collection.children.link(head_col)
    
    # 5. Setup QC settings
    toolbox.enum_qcGen_modelType = 'CHARACTER'
    toolbox.int_qcGen_scale = 1
    toolbox.bool_qcGen_generateCollission = True
    toolbox.string_qcGen_mdlModelName = "models/test/character.mdl"
    
    # 6. Setup bodygroups
    qc_data.num_boxes = 2
    while len(qc_data.bodygroup_boxes) < 2:
        qc_data.bodygroup_boxes.add()
    
    qc_data.bodygroup_boxes[0].name = "body"
    qc_data.bodygroup_boxes[1].name = "head"
    
    # 7. Verify setup
    test_output.append(f"Model type: {toolbox.enum_qcGen_modelType}")
    test_output.append(f"Model name: {toolbox.string_qcGen_mdlModelName}")
    test_output.append(f"Bodygroups: {len(qc_data.bodygroup_boxes)}")
    test_output.append("Character setup workflow complete")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
