"""
Integration tests for Material to VTF feature.
These tests require Blender to be installed.

Run with: pytest tests/test_material_vtf_integration.py -v -m integration
"""
import pytest
from pathlib import Path
import sys

# Add tests directory to path
sys.path.insert(0, str(Path(__file__).parent))

from conftest import (
    run_addon_test_in_blender,
    blender_available,
    requires_blender,
    integration,
)


@pytest.mark.integration
@requires_blender
class TestMaterialVTFPropertyRegistration:
    """Test that Material VTF properties are properly registered."""
    
    def test_mats_collection_property_exists(self):
        """Test that von_mats_collection property is registered on Scene."""
        result = run_addon_test_in_blender('''
    if hasattr(bpy.types.Scene, 'von_mats_collection'):
        test_output.append("von_mats_collection property found")
    else:
        raise AssertionError("von_mats_collection property not found on Scene")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_vtfcmd_path_property_exists(self):
        """Test that von_vtfcmd_path property is registered."""
        result = run_addon_test_in_blender('''
    if hasattr(bpy.types.Scene, 'von_vtfcmd_path'):
        test_output.append("von_vtfcmd_path property found")
    else:
        raise AssertionError("von_vtfcmd_path property not found on Scene")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_material_output_path_property_exists(self):
        """Test that von_material_output_path property is registered."""
        result = run_addon_test_in_blender('''
    if hasattr(bpy.types.Scene, 'von_material_output_path'):
        test_output.append("von_material_output_path property found")
    else:
        raise AssertionError("von_material_output_path property not found on Scene")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_vtf_format_property_exists(self):
        """Test that VTF format enum property is registered."""
        result = run_addon_test_in_blender('''
    scene = bpy.context.scene
    
    # Check the property exists and has valid values
    vtf_format = scene.von_vtf_format
    
    valid_formats = ['dxt1', 'dxt3', 'dxt5']
    if vtf_format in valid_formats:
        test_output.append(f"VTF format: {vtf_format}")
    else:
        raise AssertionError(f"Invalid VTF format: {vtf_format}")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_vmt_shader_property_exists(self):
        """Test that VMT shader enum property is registered."""
        result = run_addon_test_in_blender('''
    scene = bpy.context.scene
    
    vmt_shader = scene.von_vmt_shader
    
    valid_shaders = ['UnlitGeneric', 'VertexlitGeneric', 'LightmappedGeneric']
    if vmt_shader in valid_shaders:
        test_output.append(f"VMT shader: {vmt_shader}")
    else:
        raise AssertionError(f"Invalid VMT shader: {vmt_shader}")
''')
        
        assert result['success'], f"Test failed: {result['error']}"


@pytest.mark.integration
@requires_blender
class TestMaterialVTFOperatorRegistration:
    """Test that Material VTF operators are properly registered."""
    
    def test_refresh_materials_operator_exists(self):
        """Test that refresh materials operator is registered."""
        result = run_addon_test_in_blender('''
    if hasattr(bpy.ops.von, 'vtf_refresh_materials'):
        test_output.append("vtf_refresh_materials operator found")
    else:
        raise AssertionError("vtf_refresh_materials operator not found")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_convert_materials_operator_exists(self):
        """Test that convert materials operator is registered."""
        result = run_addon_test_in_blender('''
    if hasattr(bpy.ops.von, 'vtf_convert_materials'):
        test_output.append("vtf_convert_materials operator found")
    else:
        raise AssertionError("vtf_convert_materials operator not found")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_select_all_operator_exists(self):
        """Test that select all operator is registered."""
        result = run_addon_test_in_blender('''
    if hasattr(bpy.ops.von, 'vtf_select_all'):
        test_output.append("vtf_select_all operator found")
    else:
        raise AssertionError("vtf_select_all operator not found")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_deselect_all_operator_exists(self):
        """Test that deselect all operator is registered."""
        result = run_addon_test_in_blender('''
    if hasattr(bpy.ops.von, 'vtf_deselect_all'):
        test_output.append("vtf_deselect_all operator found")
    else:
        raise AssertionError("vtf_deselect_all operator not found")
''')
        
        assert result['success'], f"Test failed: {result['error']}"


@pytest.mark.integration
@requires_blender
class TestMaterialVTFUIRegistration:
    """Test that Material VTF UI panels are properly registered."""
    
    def test_material_list_ui_registered(self):
        """Test that material list UI is registered."""
        result = run_addon_test_in_blender('''
    # Check if UI list class is registered
    ui_list_id = "VON_UL_MaterialList"
    
    found = False
    for name in dir(bpy.types):
        if name == ui_list_id:
            found = True
            break
    
    if found:
        test_output.append(f"UI list {ui_list_id} found")
    else:
        raise AssertionError(f"UI list {ui_list_id} not found")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_vmt_generator_panel_registered(self):
        """Test that VMT generator panel is registered."""
        result = run_addon_test_in_blender('''
    panel_id = "VON_PT_vmt_generator"
    
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
    
    def test_vmt_material_settings_panel_registered(self):
        """Test that VMT material settings panel is registered."""
        result = run_addon_test_in_blender('''
    panel_id = "VON_PT_vmt_material_settings"
    
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
class TestMaterialVTFWorkflow:
    """Test Material VTF workflow functionality."""
    
    def test_refresh_materials_with_material(self):
        """Test refreshing materials list with a material in scene."""
        result = run_addon_test_in_blender('''
    # Create a cube with a material
    bpy.ops.mesh.primitive_cube_add()
    cube = bpy.context.active_object
    
    # Create material
    mat = bpy.data.materials.new(name="TestMaterial")
    mat.use_nodes = True
    
    # Assign material to cube
    cube.data.materials.append(mat)
    
    # Refresh materials list
    bpy.ops.von.vtf_refresh_materials()
    
    # Check that material was added to collection
    scene = bpy.context.scene
    if len(scene.von_mats_collection) == 1:
        test_output.append("Material correctly added to collection")
        test_output.append(f"Material name: {scene.von_mats_collection[0].material_name}")
    else:
        raise AssertionError(f"Expected 1 material, got {len(scene.von_mats_collection)}")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_select_deselect_all_materials(self):
        """Test select and deselect all functionality."""
        result = run_addon_test_in_blender('''
    # Create multiple objects with materials
    for i in range(3):
        bpy.ops.mesh.primitive_cube_add()
        cube = bpy.context.active_object
        mat = bpy.data.materials.new(name=f"Material_{i}")
        cube.data.materials.append(mat)
    
    # Refresh materials list
    bpy.ops.von.vtf_refresh_materials()
    
    scene = bpy.context.scene
    
    # Verify all are selected by default
    all_selected = all(item.material_checkbox for item in scene.von_mats_collection)
    if not all_selected:
        raise AssertionError("Materials should be selected by default")
    
    # Deselect all
    bpy.ops.von.vtf_deselect_all()
    
    all_deselected = not any(item.material_checkbox for item in scene.von_mats_collection)
    if not all_deselected:
        raise AssertionError("Deselect all failed")
    
    # Select all
    bpy.ops.von.vtf_select_all()
    
    all_selected_again = all(item.material_checkbox for item in scene.von_mats_collection)
    if not all_selected_again:
        raise AssertionError("Select all failed")
    
    test_output.append(f"Successfully tested select/deselect with {len(scene.von_mats_collection)} materials")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_vmt_parameters_on_material(self):
        """Test that VMT parameters are accessible on material list items."""
        result = run_addon_test_in_blender('''
    # Create object with material
    bpy.ops.mesh.primitive_cube_add()
    cube = bpy.context.active_object
    mat = bpy.data.materials.new(name="VMTTestMaterial")
    cube.data.materials.append(mat)
    
    # Refresh materials list
    bpy.ops.von.vtf_refresh_materials()
    
    scene = bpy.context.scene
    
    if len(scene.von_mats_collection) > 0:
        mat_item = scene.von_mats_collection[0]
        vmt_params = mat_item.vmt_params
        
        # Test setting various VMT parameters
        vmt_params.enable_phong = True
        vmt_params.phong_boost = 2.0
        vmt_params.enable_rimlight = True
        vmt_params.rimlight_exponent = 50.0
        vmt_params.enable_envmap = True
        
        # Verify values were set
        if vmt_params.phong_boost != 2.0:
            raise AssertionError(f"Phong boost not set correctly: {vmt_params.phong_boost}")
        if vmt_params.rimlight_exponent != 50.0:
            raise AssertionError(f"Rimlight exponent not set correctly: {vmt_params.rimlight_exponent}")
        
        test_output.append("VMT parameters successfully configured")
    else:
        raise AssertionError("No materials in collection")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_vtf_settings_configuration(self):
        """Test configuring VTF conversion settings."""
        result = run_addon_test_in_blender('''
    scene = bpy.context.scene
    
    # Test setting VTF format options
    scene.von_vtf_format = 'dxt1'
    if scene.von_vtf_format != 'dxt1':
        raise AssertionError("VTF format not set correctly")
    
    scene.von_vtf_format = 'dxt5'
    if scene.von_vtf_format != 'dxt5':
        raise AssertionError("VTF format not set correctly to dxt5")
    
    # Test VTF version
    scene.von_vtf_version = '7.3'
    if scene.von_vtf_version != '7.3':
        raise AssertionError("VTF version not set correctly")
    
    # Test resize settings
    scene.von_vtf_resize_bool = True
    scene.von_vtf_clamp_size = '1024x1024'
    if scene.von_vtf_clamp_size != '1024x1024':
        raise AssertionError("Clamp size not set correctly")
    
    # Test VMT generation toggle
    scene.von_vmt_generate_bool = True
    scene.von_vmt_shader = 'LightmappedGeneric'
    if scene.von_vmt_shader != 'LightmappedGeneric':
        raise AssertionError("VMT shader not set correctly")
    
    test_output.append("VTF settings configuration successful")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
    
    def test_multiple_materials_workflow(self):
        """Test workflow with multiple materials."""
        result = run_addon_test_in_blender('''
    # Create multiple objects with different materials
    material_names = ["Head", "Body", "Hands", "Feet"]
    
    for name in material_names:
        bpy.ops.mesh.primitive_cube_add()
        obj = bpy.context.active_object
        obj.name = f"{name}_Mesh"
        
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        obj.data.materials.append(mat)
    
    # Refresh materials list
    bpy.ops.von.vtf_refresh_materials()
    
    scene = bpy.context.scene
    
    # Verify all materials were collected
    if len(scene.von_mats_collection) != len(material_names):
        raise AssertionError(f"Expected {len(material_names)} materials, got {len(scene.von_mats_collection)}")
    
    # Configure each material's VMT settings
    for i, mat_item in enumerate(scene.von_mats_collection):
        vmt_params = mat_item.vmt_params
        vmt_params.enable_phong = True
        vmt_params.phong_boost = 1.0 + (i * 0.5)
    
    # Verify settings were saved
    for i, mat_item in enumerate(scene.von_mats_collection):
        expected_boost = 1.0 + (i * 0.5)
        actual_boost = mat_item.vmt_params.phong_boost
        if abs(actual_boost - expected_boost) > 0.01:
            raise AssertionError(f"Material {i} phong_boost incorrect: {actual_boost} != {expected_boost}")
    
    test_output.append(f"Successfully managed {len(material_names)} materials with unique settings")
''')
        
        assert result['success'], f"Test failed: {result['error']}"
