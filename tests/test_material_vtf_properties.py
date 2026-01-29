"""
Unit tests for the material_vtf_properties module.
"""
import pytest
from pathlib import Path
import sys
from unittest.mock import MagicMock, patch

# Add the refactor directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "refactor"))


class TestVMTParametersPropertyGroup:
    """Tests for VMT_Parameters property group."""
    
    def test_vmt_parameters_class_exists(self, mock_bpy):
        """Test that VMT_Parameters class is defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.PropertyGroup = type('PropertyGroup', (), {})
            mock_bpy.types.Image = type('Image', (), {})
            
            from properties.material_vtf_properties import VMT_Parameters
            
            assert VMT_Parameters is not None
    
    def test_vmt_parameters_has_phong_properties(self, mock_bpy):
        """Test that VMT_Parameters has phong-related properties."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.PropertyGroup = type('PropertyGroup', (), {})
            mock_bpy.types.Image = type('Image', (), {})
            
            from properties.material_vtf_properties import VMT_Parameters
            
            # Check annotations for property definitions
            annotations = VMT_Parameters.__annotations__
            
            assert 'enable_phong' in annotations
            assert 'phong_boost' in annotations
            assert 'phong_albedo_tint' in annotations
            assert 'phong_albedo_boost' in annotations
            assert 'phong_fresnel_ranges' in annotations
    
    def test_vmt_parameters_has_rimlight_properties(self, mock_bpy):
        """Test that VMT_Parameters has rim lighting properties."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.PropertyGroup = type('PropertyGroup', (), {})
            mock_bpy.types.Image = type('Image', (), {})
            
            from properties.material_vtf_properties import VMT_Parameters
            
            annotations = VMT_Parameters.__annotations__
            
            assert 'enable_rimlight' in annotations
            assert 'rimlight_exponent' in annotations
            assert 'rimlight_boost' in annotations
            assert 'rim_mask' in annotations
    
    def test_vmt_parameters_has_envmap_properties(self, mock_bpy):
        """Test that VMT_Parameters has environment mapping properties."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.PropertyGroup = type('PropertyGroup', (), {})
            mock_bpy.types.Image = type('Image', (), {})
            
            from properties.material_vtf_properties import VMT_Parameters
            
            annotations = VMT_Parameters.__annotations__
            
            assert 'enable_envmap' in annotations
            assert 'envmap_tint' in annotations
            assert 'normal_map_alpha_envmap_mask' in annotations
    
    def test_vmt_parameters_has_texture_maps(self, mock_bpy):
        """Test that VMT_Parameters has texture map properties."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.PropertyGroup = type('PropertyGroup', (), {})
            mock_bpy.types.Image = type('Image', (), {})
            
            from properties.material_vtf_properties import VMT_Parameters
            
            annotations = VMT_Parameters.__annotations__
            
            assert 'normal_map' in annotations
            assert 'phong_exponent_map' in annotations


class TestMaterialListItemPropertyGroup:
    """Tests for VMT_MaterialListItem property group."""
    
    def test_material_list_item_class_exists(self, mock_bpy):
        """Test that VMT_MaterialListItem class is defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.PropertyGroup = type('PropertyGroup', (), {})
            mock_bpy.types.Image = type('Image', (), {})
            mock_bpy.types.Material = type('Material', (), {})
            
            from properties.material_vtf_properties import VMT_MaterialListItem
            
            assert VMT_MaterialListItem is not None
    
    def test_material_list_item_has_required_properties(self, mock_bpy):
        """Test that VMT_MaterialListItem has all required properties."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.PropertyGroup = type('PropertyGroup', (), {})
            mock_bpy.types.Image = type('Image', (), {})
            mock_bpy.types.Material = type('Material', (), {})
            
            from properties.material_vtf_properties import VMT_MaterialListItem
            
            annotations = VMT_MaterialListItem.__annotations__
            
            assert 'material_checkbox' in annotations
            assert 'material_name' in annotations
            assert 'material' in annotations
            assert 'vmt_params' in annotations


class TestPathSettingsPropertyGroup:
    """Tests for VMT_PathSettings property group."""
    
    def test_path_settings_class_exists(self, mock_bpy):
        """Test that VMT_PathSettings class is defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.PropertyGroup = type('PropertyGroup', (), {})
            mock_bpy.types.Image = type('Image', (), {})
            
            from properties.material_vtf_properties import VMT_PathSettings
            
            assert VMT_PathSettings is not None
    
    def test_path_settings_has_path_property(self, mock_bpy):
        """Test that VMT_PathSettings has path property."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.PropertyGroup = type('PropertyGroup', (), {})
            mock_bpy.types.Image = type('Image', (), {})
            
            from properties.material_vtf_properties import VMT_PathSettings
            
            annotations = VMT_PathSettings.__annotations__
            
            assert 'path' in annotations


class TestMaterialVTFPropertiesModule:
    """Tests for material_vtf_properties module structure."""
    
    def test_classes_list_defined(self, mock_bpy):
        """Test that CLASSES list is defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.PropertyGroup = type('PropertyGroup', (), {})
            mock_bpy.types.Image = type('Image', (), {})
            mock_bpy.types.Material = type('Material', (), {})
            
            from properties.material_vtf_properties import CLASSES
            
            assert isinstance(CLASSES, list)
            assert len(CLASSES) == 3
    
    def test_register_function_exists(self, mock_bpy):
        """Test that register function is defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.PropertyGroup = type('PropertyGroup', (), {})
            mock_bpy.types.Image = type('Image', (), {})
            mock_bpy.types.Material = type('Material', (), {})
            
            from properties.material_vtf_properties import register, unregister
            
            assert callable(register)
            assert callable(unregister)
    
    def test_scene_properties_functions_exist(self, mock_bpy):
        """Test that scene property registration functions exist."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.PropertyGroup = type('PropertyGroup', (), {})
            mock_bpy.types.Image = type('Image', (), {})
            mock_bpy.types.Material = type('Material', (), {})
            
            from properties.material_vtf_properties import (
                register_scene_properties,
                unregister_scene_properties
            )
            
            assert callable(register_scene_properties)
            assert callable(unregister_scene_properties)
