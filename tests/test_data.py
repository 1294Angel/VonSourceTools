"""
Unit tests for the data module.
These tests don't require Blender.
"""
import pytest
from pathlib import Path
import sys

# Add the refactor directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "refactor"))


class TestConstants:
    """Tests for data/constants.py"""
    
    def test_model_type_category_map_exists(self):
        """Test that MODEL_TYPE_CATEGORY_MAP is defined."""
        from data.constants import MODEL_TYPE_CATEGORY_MAP
        
        assert MODEL_TYPE_CATEGORY_MAP is not None
        assert isinstance(MODEL_TYPE_CATEGORY_MAP, dict)
    
    def test_model_type_category_map_has_required_keys(self):
        """Test that all model types are defined."""
        from data.constants import MODEL_TYPE_CATEGORY_MAP
        
        required_types = ['NPC', 'CHARACTER', 'VIEWMODEL', 'PROP', 'WORLDMODEL']
        for model_type in required_types:
            assert model_type in MODEL_TYPE_CATEGORY_MAP, f"Missing model type: {model_type}"
    
    def test_npc_and_character_have_same_categories(self):
        """Test that NPC and CHARACTER have matching categories."""
        from data.constants import MODEL_TYPE_CATEGORY_MAP
        
        assert MODEL_TYPE_CATEGORY_MAP['NPC'] == MODEL_TYPE_CATEGORY_MAP['CHARACTER']
    
    def test_none_enum_format(self):
        """Test that NONE_ENUM has correct format for Blender."""
        from data.constants import NONE_ENUM
        
        assert isinstance(NONE_ENUM, tuple)
        assert len(NONE_ENUM) == 3
        assert NONE_ENUM[0] == "NONE"


class TestValveBipedBones:
    """Tests for data/valvebiped_bones.py"""
    
    def test_valvebiped_bones_is_list(self):
        """Test that VALVEBIPED_BONES is a list."""
        from data.valvebiped_bones import VALVEBIPED_BONES
        
        assert isinstance(VALVEBIPED_BONES, list)
        assert len(VALVEBIPED_BONES) > 0
    
    def test_valvebiped_bones_contain_pelvis(self):
        """Test that pelvis bone is in the list."""
        from data.valvebiped_bones import VALVEBIPED_BONES
        
        assert 'ValveBiped.Bip01_Pelvis' in VALVEBIPED_BONES
    
    def test_valvebiped_bones_contain_required_bones(self):
        """Test that essential bones are present."""
        from data.valvebiped_bones import VALVEBIPED_BONES
        
        required_bones = [
            'ValveBiped.Bip01_Pelvis',
            'ValveBiped.Bip01_Spine',
            'ValveBiped.Bip01_Head1',
            'ValveBiped.Bip01_L_Hand',
            'ValveBiped.Bip01_R_Hand',
            'ValveBiped.Bip01_L_Foot',
            'ValveBiped.Bip01_R_Foot',
        ]
        
        for bone in required_bones:
            assert bone in VALVEBIPED_BONES, f"Missing required bone: {bone}"
    
    def test_constraint_pairs_is_list(self):
        """Test that VALVEBIPED_CONSTRAINT_PAIRS is a list."""
        from data.valvebiped_bones import VALVEBIPED_CONSTRAINT_PAIRS
        
        assert isinstance(VALVEBIPED_CONSTRAINT_PAIRS, list)
        assert len(VALVEBIPED_CONSTRAINT_PAIRS) > 0
    
    def test_constraint_pairs_even_length(self):
        """Test that constraint pairs has even length (pairs of bones)."""
        from data.valvebiped_bones import VALVEBIPED_CONSTRAINT_PAIRS
        
        # The list is used as pairs, so length should be even
        assert len(VALVEBIPED_CONSTRAINT_PAIRS) % 2 == 0


class TestPaths:
    """Tests for data/paths.py"""
    
    def test_get_addon_directory_returns_path(self):
        """Test that get_addon_directory returns a Path object."""
        from data.paths import get_addon_directory
        
        result = get_addon_directory()
        assert isinstance(result, Path)
    
    def test_get_data_directory_returns_path(self):
        """Test that get_data_directory returns a Path object."""
        from data.paths import get_data_directory
        
        result = get_data_directory()
        assert isinstance(result, Path)
        assert result.name == "storeditems"
    
    def test_armature_file_locations_returns_dict(self):
        """Test that get_armature_file_locations returns expected structure."""
        from data.paths import get_armature_file_locations
        
        result = get_armature_file_locations()
        assert isinstance(result, dict)
        assert 'proportions' in result
        assert 'reference_female' in result
        assert 'reference_male' in result
    
    def test_armature_file_locations_are_paths(self):
        """Test that armature locations are Path objects."""
        from data.paths import get_armature_file_locations
        
        result = get_armature_file_locations()
        for name, path in result.items():
            assert isinstance(path, Path), f"{name} is not a Path"
            assert path.suffix == '.fbx', f"{name} doesn't have .fbx extension"
    
    def test_templates_directory_exists(self):
        """Test that templates directory path is valid."""
        from data.paths import get_templates_directory
        
        result = get_templates_directory()
        assert isinstance(result, Path)
        # Check the path structure
        assert "templates" in str(result)


class TestDataModuleExports:
    """Tests for data/__init__.py exports."""
    
    def test_all_exports_available(self):
        """Test that all expected exports are available from data module."""
        from data import (
            MODEL_TYPE_CATEGORY_MAP,
            NONE_ENUM,
            VALVEBIPED_BONES,
            VALVEBIPED_CONSTRAINT_PAIRS,
            get_addon_directory,
            get_data_directory,
            get_armature_file_locations,
        )
        
        # Just checking they can be imported
        assert MODEL_TYPE_CATEGORY_MAP is not None
        assert NONE_ENUM is not None
        assert VALVEBIPED_BONES is not None
        assert VALVEBIPED_CONSTRAINT_PAIRS is not None
        assert callable(get_addon_directory)
        assert callable(get_data_directory)
        assert callable(get_armature_file_locations)
