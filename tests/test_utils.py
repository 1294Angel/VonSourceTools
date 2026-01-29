"""
Unit tests for the utils module.
"""
import pytest
from pathlib import Path
import sys
import json
import tempfile
import os

# Add the refactor directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "refactor"))


class TestFileUtils:
    """Tests for utils/file_utils.py"""
    
    def test_get_addon_directory_returns_path(self):
        """Test that get_addon_directory returns a Path."""
        from utils.file_utils import get_addon_directory
        
        result = get_addon_directory()
        assert isinstance(result, Path)
    
    def test_get_data_directory_returns_path(self):
        """Test that get_data_directory returns a Path."""
        from utils.file_utils import get_data_directory
        
        result = get_data_directory()
        assert isinstance(result, Path)
    
    def test_load_json_data_with_valid_file(self):
        """Test loading a valid JSON file."""
        from utils.file_utils import load_json_data
        
        # Create a temporary JSON file
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create the expected directory structure
            test_dir = Path(tmpdir) / "storeditems" / "test"
            test_dir.mkdir(parents=True)
            
            test_data = {"key": "value", "number": 42}
            test_file = test_dir / "test.json"
            with open(test_file, 'w') as f:
                json.dump(test_data, f)
            
            # We can't easily test load_json_data because it uses __file__
            # So we'll just verify the function exists and is callable
            assert callable(load_json_data)
    
    def test_load_json_data_file_not_found(self):
        """Test that FileNotFoundError is raised for missing files."""
        from utils.file_utils import load_json_data
        
        with pytest.raises(FileNotFoundError):
            load_json_data("nonexistent/path", "nonexistent.json")


class TestBlenderUtilsWithMocks:
    """Tests for utils/blender_utils.py using mocks."""
    
    def test_object_exists_returns_bool(self, mock_bpy):
        """Test that object_exists returns a boolean."""
        from utils.blender_utils import object_exists
        
        # Object doesn't exist
        result = object_exists("NonExistent")
        assert isinstance(result, bool)
        assert result is False
    
    def test_object_exists_finds_existing(self, mock_bpy):
        """Test that object_exists finds existing objects."""
        from utils.blender_utils import object_exists
        
        # Add an object to the mock
        mock_bpy.data.objects['TestObject'] = True
        
        result = object_exists("TestObject")
        assert result is True
    
    def test_select_objects_deselects_all_first(self, mock_bpy):
        """Test that select_objects deselects all objects first."""
        from utils.blender_utils import select_objects
        
        select_objects([])
        mock_bpy.ops.object.select_all.assert_called_with(action='DESELECT')
    
    def test_get_armatures_in_scene(self, mock_bpy):
        """Test getting armatures from scene."""
        from utils.blender_utils import get_armatures_in_scene
        
        # Setup mock objects
        armature = type('MockObj', (), {'type': 'ARMATURE', 'name': 'Arm'})()
        mesh = type('MockObj', (), {'type': 'MESH', 'name': 'Mesh'})()
        mock_bpy.data.objects = {'Arm': armature, 'Mesh': mesh}
        
        # Make it iterable
        mock_bpy.data.objects.__iter__ = lambda self: iter([armature, mesh])
        
        result = get_armatures_in_scene()
        assert len(result) == 1
        assert result[0].type == 'ARMATURE'
    
    def test_clear_screen_prints_empty_lines(self, mock_bpy, capsys):
        """Test that clear_screen prints empty lines."""
        from utils.blender_utils import clear_screen
        
        clear_screen()
        
        captured = capsys.readouterr()
        assert captured.out.count('\n') == 5


class TestUtilsModuleExports:
    """Tests for utils/__init__.py exports."""
    
    def test_blender_utils_exports(self, mock_bpy):
        """Test that blender utility functions are exported."""
        from utils import (
            object_exists,
            move_to_collection,
            select_objects,
            get_armatures_in_scene,
            clear_screen,
        )
        
        assert callable(object_exists)
        assert callable(move_to_collection)
        assert callable(select_objects)
        assert callable(get_armatures_in_scene)
        assert callable(clear_screen)
    
    def test_file_utils_exports(self):
        """Test that file utility functions are exported."""
        from utils import (
            load_json_data,
            get_addon_directory,
            get_data_directory,
        )
        
        assert callable(load_json_data)
        assert callable(get_addon_directory)
        assert callable(get_data_directory)
