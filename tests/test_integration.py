"""
Integration tests that run inside Blender.
These tests require Blender to be installed.

Run with: pytest tests/test_integration.py -v -m integration
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
    integration,
    ADDON_PATH,
)


@pytest.mark.integration
@requires_blender
class TestAddonRegistration:
    """Test that the addon registers and unregisters correctly."""
    
    def test_addon_registers_without_error(self):
        """Test that the addon can be registered."""
        result = run_addon_test_in_blender('''
    test_output.append("Addon registered successfully")
''')
        
        assert result['success'], f"Registration failed: {result['error']}"
    
    def test_addon_unregisters_without_error(self):
        """Test that the addon unregisters cleanly."""
        result = run_addon_test_in_blender('''
    # Registration/unregistration happens in the wrapper
    test_output.append("Addon unregistered successfully")
''')
        
        assert result['success'], f"Unregistration failed: {result['error']}"


@pytest.mark.integration
@requires_blender
class TestPropertyGroups:
    """Test that property groups are properly registered."""
    
    def test_toolbox_property_exists(self):
        """Test that toolBox property is registered on Scene."""
        result = run_addon_test_in_blender('''
    if hasattr(bpy.types.Scene, 'toolBox'):
        test_output.append("toolBox property found")
    else:
        raise AssertionError("toolBox property not found on Scene")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_qc_primary_data_exists(self):
        """Test that QC_PrimaryData property is registered."""
        result = run_addon_test_in_blender('''
    if hasattr(bpy.types.Scene, 'QC_PrimaryData'):
        test_output.append("QC_PrimaryData property found")
    else:
        raise AssertionError("QC_PrimaryData property not found on Scene")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_toolbox_has_delta_anim_threshold(self):
        """Test that toolBox has delta animation threshold property."""
        result = run_addon_test_in_blender('''
    scene = bpy.context.scene
    toolbox = scene.toolBox
    
    # Check the property exists and has a default value
    threshold = toolbox.float_deltaAnim_similarityThreshold
    test_output.append(f"Threshold value: {threshold}")
    
    if threshold != 90.0:
        raise AssertionError(f"Expected default 90.0, got {threshold}")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_toolbox_has_qc_model_type(self):
        """Test that toolBox has QC model type enum."""
        result = run_addon_test_in_blender('''
    scene = bpy.context.scene
    toolbox = scene.toolBox
    
    model_type = toolbox.enum_qcGen_modelType
    test_output.append(f"Model type: {model_type}")
    
    valid_types = ['PROP', 'CHARACTER', 'NPC', 'VIEWMODEL', 'WORLDMODEL']
    if model_type not in valid_types:
        raise AssertionError(f"Invalid model type: {model_type}")
''')
        
        assert result['success'], f"Test failed: {result['error']}"


@pytest.mark.integration
@requires_blender
class TestOperators:
    """Test that operators are properly registered."""
    
    def test_delta_anim_full_operator_exists(self):
        """Test that delta animation full operator is registered."""
        result = run_addon_test_in_blender('''
    # Check if operator is registered
    if hasattr(bpy.ops.von, 'deltaanimtrick_full'):
        test_output.append("Delta anim full operator found")
    else:
        raise AssertionError("Delta anim full operator not found")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_collect_sequences_operator_exists(self):
        """Test that collect sequences operator is registered."""
        result = run_addon_test_in_blender('''
    if hasattr(bpy.ops.von, 'collect_sequences'):
        test_output.append("Collect sequences operator found")
    else:
        raise AssertionError("Collect sequences operator not found")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_refresh_collections_operator_exists(self):
        """Test that refresh collections operator is registered."""
        result = run_addon_test_in_blender('''
    if hasattr(bpy.ops.von, 'qcgenerator_refresh_collections'):
        test_output.append("Refresh collections operator found")
    else:
        raise AssertionError("Refresh collections operator not found")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_batch_convert_operator_exists(self):
        """Test that batch convert operator is registered."""
        result = run_addon_test_in_blender('''
    if hasattr(bpy.ops.von, 'batchconvertfiletypes'):
        test_output.append("Batch convert operator found")
    else:
        raise AssertionError("Batch convert operator not found")
''')
        
        assert result['success'], f"Test failed: {result['error']}"


@pytest.mark.integration
@requires_blender
class TestPanels:
    """Test that UI panels are properly registered."""
    
    def test_parent_panel_registered(self):
        """Test that the parent panel is registered."""
        result = run_addon_test_in_blender('''
    # Check if panel class is registered
    panel_id = "VON_PT_parent"
    
    # Try to find panel in registered types
    found = False
    for name in dir(bpy.types):
        if name == panel_id:
            found = True
            break
    
    if found:
        test_output.append(f"Panel {panel_id} found")
    else:
        raise AssertionError(f"Panel {panel_id} not found")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_qc_generator_panel_registered(self):
        """Test that QC generator panel is registered."""
        result = run_addon_test_in_blender('''
    panel_id = "VON_PT_qc_generator_main"
    
    found = False
    for name in dir(bpy.types):
        if name == panel_id:
            found = True
            break
    
    if found:
        test_output.append(f"Panel {panel_id} found")
    else:
        raise AssertionError(f"Panel {panel_id} not found")
''')
        
        assert result['success'], f"Test failed: {result['error']}"


@pytest.mark.integration
@requires_blender
class TestBlenderDataAccess:
    """Test that the addon can access Blender data correctly."""
    
    def test_can_create_armature(self):
        """Test that we can create an armature in Blender."""
        result = run_addon_test_in_blender('''
    # Create a simple armature
    bpy.ops.object.armature_add()
    
    armature = bpy.context.active_object
    if armature and armature.type == 'ARMATURE':
        test_output.append(f"Created armature: {armature.name}")
    else:
        raise AssertionError("Failed to create armature")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_can_create_collection(self):
        """Test that we can create a collection."""
        result = run_addon_test_in_blender('''
    col_name = "TestCollection"
    new_col = bpy.data.collections.new(col_name)
    bpy.context.scene.collection.children.link(new_col)
    
    if col_name in bpy.data.collections:
        test_output.append(f"Created collection: {col_name}")
    else:
        raise AssertionError("Failed to create collection")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_bodygroup_box_management(self):
        """Test that bodygroup boxes can be managed."""
        result = run_addon_test_in_blender('''
    scene = bpy.context.scene
    qc_data = scene.QC_PrimaryData
    
    # Set number of bodygroups
    qc_data.num_boxes = 2
    
    # Manually add boxes (sync function would normally do this)
    while len(qc_data.bodygroup_boxes) < qc_data.num_boxes:
        qc_data.bodygroup_boxes.add()
    
    # Verify
    if len(qc_data.bodygroup_boxes) == 2:
        test_output.append("Successfully created 2 bodygroup boxes")
    else:
        raise AssertionError(f"Expected 2 boxes, got {len(qc_data.bodygroup_boxes)}")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
