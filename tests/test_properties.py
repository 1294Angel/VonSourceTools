"""
Unit tests for the properties module.
These test property group definitions and helper functions.
"""
import pytest
from pathlib import Path
import sys
from unittest.mock import MagicMock, patch

# Add the refactor directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "refactor"))


class TestToolboxPropertiesHelpers:
    """Tests for helper functions in toolbox_properties.py"""
    
    def test_populate_filetypes_returns_list(self, mock_bpy):
        """Test that populate_filetypes_to_vtf returns a list of tuples."""
        # We need to import with mocked bpy
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            # Import the dependent modules first
            with patch.dict(sys.modules, {
                'bpy.props': MagicMock(),
            }):
                from properties.toolbox_properties import populate_filetypes_to_vtf
                
                result = populate_filetypes_to_vtf(None, None)
                
                assert isinstance(result, list)
                assert len(result) > 0
                
                # Check format of items
                for item in result:
                    assert isinstance(item, tuple)
                    assert len(item) == 3
    
    def test_populate_filetypes_contains_required_formats(self, mock_bpy):
        """Test that all required formats are present."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            with patch.dict(sys.modules, {
                'bpy.props': MagicMock(),
            }):
                from properties.toolbox_properties import populate_filetypes_to_vtf
                
                result = populate_filetypes_to_vtf(None, None)
                extensions = [item[0] for item in result]
                
                required = ['png', 'jpg', 'tga', 'vtf']
                for ext in required:
                    assert ext in extensions, f"Missing format: {ext}"


class TestSyncBodygroupBoxes:
    """Tests for sync_bodygroup_boxes function."""
    
    def test_sync_adds_boxes(self, mock_bpy):
        """Test that sync_bodygroup_boxes adds boxes when needed."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            with patch.dict(sys.modules, {
                'bpy.props': MagicMock(),
            }):
                # Create mock scene and qc_data
                scene = MagicMock()
                qc_data = MagicMock()
                scene.QC_PrimaryData = qc_data
                
                # Setup bodygroup boxes as a list-like mock
                boxes = []
                qc_data.bodygroup_boxes = boxes
                qc_data.bodygroup_boxes.__len__ = lambda: len(boxes)
                qc_data.bodygroup_boxes.add = lambda: boxes.append(MagicMock())
                qc_data.bodygroup_boxes.remove = lambda i: boxes.pop(i)
                
                qc_data.num_boxes = 3
                
                # Mock collections
                mock_bpy.data.collections = []
                
                from properties.toolbox_properties import sync_bodygroup_boxes
                
                sync_bodygroup_boxes(scene)
                
                assert len(boxes) == 3


class TestGetBodygroupByName:
    """Tests for get_bodygroup_by_name function."""
    
    def test_finds_existing_bodygroup(self, mock_bpy):
        """Test finding an existing bodygroup by name."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            with patch.dict(sys.modules, {
                'bpy.props': MagicMock(),
            }):
                from properties.toolbox_properties import get_bodygroup_by_name
                
                # Create mock qc_data with bodygroups
                qc_data = MagicMock()
                box1 = MagicMock()
                box1.name = "Head"
                box2 = MagicMock()
                box2.name = "Body"
                qc_data.bodygroup_boxes = [box1, box2]
                
                result = get_bodygroup_by_name(qc_data, "Head")
                assert result == box1
                
                result = get_bodygroup_by_name(qc_data, "Body")
                assert result == box2
    
    def test_returns_none_for_missing(self, mock_bpy):
        """Test that None is returned for missing bodygroup."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            with patch.dict(sys.modules, {
                'bpy.props': MagicMock(),
            }):
                from properties.toolbox_properties import get_bodygroup_by_name
                
                qc_data = MagicMock()
                qc_data.bodygroup_boxes = []
                
                result = get_bodygroup_by_name(qc_data, "NonExistent")
                assert result is None


class TestPropertyClassDefinitions:
    """Test that property classes are properly defined."""
    
    def test_qc_properties_classes_exist(self, mock_bpy):
        """Test that QC property classes are defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            # Need to mock bpy.types.PropertyGroup
            mock_bpy.types.PropertyGroup = type('PropertyGroup', (), {})
            
            with patch.dict(sys.modules, {
                'bpy.props': MagicMock(),
            }):
                from properties import qc_properties
                
                assert hasattr(qc_properties, 'CLASSES')
                assert len(qc_properties.CLASSES) > 0
    
    def test_sequence_properties_classes_exist(self, mock_bpy):
        """Test that sequence property classes are defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.PropertyGroup = type('PropertyGroup', (), {})
            
            with patch.dict(sys.modules, {
                'bpy.props': MagicMock(),
            }):
                from properties import sequence_properties
                
                assert hasattr(sequence_properties, 'CLASSES')
                assert len(sequence_properties.CLASSES) > 0
    
    def test_toolbox_properties_classes_exist(self, mock_bpy):
        """Test that toolbox property classes are defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.PropertyGroup = type('PropertyGroup', (), {})
            
            with patch.dict(sys.modules, {
                'bpy.props': MagicMock(),
            }):
                from properties import toolbox_properties
                
                assert hasattr(toolbox_properties, 'CLASSES')
                assert len(toolbox_properties.CLASSES) > 0


class TestPropertiesModuleStructure:
    """Tests for properties module structure."""
    
    def test_properties_init_has_modules(self, mock_bpy):
        """Test that properties __init__ defines MODULES."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.PropertyGroup = type('PropertyGroup', (), {})
            
            with patch.dict(sys.modules, {
                'bpy.props': MagicMock(),
            }):
                from properties import MODULES
                
                assert isinstance(MODULES, list)
                assert len(MODULES) == 3  # qc, sequence, toolbox
    
    def test_properties_has_register_functions(self, mock_bpy):
        """Test that properties module has register/unregister."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.PropertyGroup = type('PropertyGroup', (), {})
            
            with patch.dict(sys.modules, {
                'bpy.props': MagicMock(),
            }):
                from properties import register, unregister
                
                assert callable(register)
                assert callable(unregister)
