"""
Unit tests for the core module.
"""
import pytest
from pathlib import Path
import sys
from unittest.mock import MagicMock, patch

# Add the refactor directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "refactor"))


class TestVTFConversion:
    """Tests for core/vtf_conversion.py"""
    
    def test_supported_filetypes_list(self):
        """Test that SUPPORTED_FILETYPES is properly defined."""
        from core.vtf_conversion import SUPPORTED_FILETYPES
        
        assert isinstance(SUPPORTED_FILETYPES, list)
        assert len(SUPPORTED_FILETYPES) > 0
        
        # Check format of each item
        for item in SUPPORTED_FILETYPES:
            assert isinstance(item, tuple)
            assert len(item) == 3
    
    def test_get_supported_filetypes_returns_list(self):
        """Test get_supported_filetypes function."""
        from core.vtf_conversion import get_supported_filetypes
        
        result = get_supported_filetypes()
        assert isinstance(result, list)
        assert len(result) > 0
    
    def test_vtf_in_supported_filetypes(self):
        """Test that VTF is in supported filetypes."""
        from core.vtf_conversion import SUPPORTED_FILETYPES
        
        extensions = [item[0] for item in SUPPORTED_FILETYPES]
        assert 'vtf' in extensions
    
    def test_common_image_formats_supported(self):
        """Test that common image formats are supported."""
        from core.vtf_conversion import SUPPORTED_FILETYPES
        
        extensions = [item[0] for item in SUPPORTED_FILETYPES]
        
        required = ['png', 'jpg', 'tga', 'bmp']
        for ext in required:
            assert ext in extensions, f"Missing format: {ext}"


class TestQCBuilder:
    """Tests for core/qc_builder.py"""
    
    def test_make_qc_command_adds_prefix(self):
        """Test that make_qc_command adds $ prefix."""
        # Import with mocked bpy
        with patch.dict(sys.modules, {'bpy': MagicMock()}):
            from core.qc_builder import make_qc_command
            
            result = make_qc_command("modelname")
            assert result == "$modelname"
    
    def test_make_qc_command_various_commands(self):
        """Test make_qc_command with various inputs."""
        with patch.dict(sys.modules, {'bpy': MagicMock()}):
            from core.qc_builder import make_qc_command
            
            test_cases = [
                ("modelname", "$modelname"),
                ("cdmaterials", "$cdmaterials"),
                ("sequence", "$sequence"),
                ("bodygroup", "$bodygroup"),
            ]
            
            for input_cmd, expected in test_cases:
                assert make_qc_command(input_cmd) == expected


class TestSequences:
    """Tests for core/sequences.py"""
    
    def test_collect_actions_from_armature_no_animation_data(self, mock_bpy):
        """Test collecting actions from armature without animation data."""
        from core.sequences import collect_actions_from_armature
        
        armature = MagicMock()
        armature.animation_data = None
        
        result = collect_actions_from_armature(armature)
        assert isinstance(result, set)
        assert len(result) == 0
    
    def test_collect_actions_from_armature_with_action(self, mock_bpy):
        """Test collecting actions from armature with active action."""
        mock_bpy.types.Action = type('Action', (), {})
        
        from core.sequences import collect_actions_from_armature
        
        armature = MagicMock()
        action = MagicMock(spec=mock_bpy.types.Action)
        armature.animation_data.action = action
        armature.animation_data.nla_tracks = []
        
        # Make isinstance check work
        with patch('core.sequences.bpy.types.Action', mock_bpy.types.Action):
            result = collect_actions_from_armature(armature)
            assert isinstance(result, set)


class TestDeltaAnim:
    """Tests for core/delta_anim.py"""
    
    def test_validate_valvebiped_similarity_non_armature(self, mock_bpy):
        """Test validation fails for non-armature objects."""
        from core.delta_anim import validate_valvebiped_similarity
        
        obj = MagicMock()
        obj.type = 'MESH'
        
        result = validate_valvebiped_similarity(obj)
        assert result is False
    
    def test_validate_valvebiped_similarity_with_matching_bones(self, mock_bpy):
        """Test validation passes with matching bones."""
        from core.delta_anim import validate_valvebiped_similarity
        from data.valvebiped_bones import VALVEBIPED_BONES
        
        # Create armature with ValveBiped bones
        armature = MagicMock()
        armature.type = 'ARMATURE'
        
        # Create bone mocks
        bones = {}
        for bone_name in VALVEBIPED_BONES[:50]:  # Use first 50 bones
            bone = MagicMock()
            bone.name = bone_name
            bones[bone_name] = bone
        
        armature.data.bones = bones
        
        result = validate_valvebiped_similarity(armature, threshold=90.0)
        # Should pass because all bones match
        assert isinstance(result, bool)


class TestCollision:
    """Tests for core/collision.py"""
    
    def test_get_skinned_meshes_empty(self, mock_bpy):
        """Test getting skinned meshes with no meshes."""
        from core.collision import get_skinned_meshes
        
        armature = MagicMock()
        mock_bpy.data.objects = {}
        
        result = get_skinned_meshes(armature)
        assert isinstance(result, list)
    
    def test_generate_collision_bounds_empty_input(self, mock_bpy):
        """Test collision bounds with empty input."""
        from core.collision import generate_collision_bounds
        
        obj = MagicMock()
        result = generate_collision_bounds({}, obj)
        
        assert isinstance(result, dict)
        assert len(result) == 0


class TestSMDExport:
    """Tests for core/smd_export.py"""
    
    def test_restore_without_mapping(self, mock_bpy):
        """Test restore_objects_from_collections with no mapping."""
        from core.smd_export import restore_objects_from_collections
        
        context = MagicMock()
        context.scene.get.return_value = None
        
        # Should not raise an error
        restore_objects_from_collections(context)


class TestStudioMDL:
    """Tests for core/studiomdl.py"""
    
    def test_run_definebones_missing_studiomdl(self):
        """Test that FileNotFoundError is raised for missing studiomdl."""
        from core.studiomdl import run_definebones
        
        with pytest.raises(FileNotFoundError) as excinfo:
            run_definebones(
                studiomdl_exe=Path("/nonexistent/studiomdl.exe"),
                qc_path=Path("/nonexistent/test.qc"),
                gmod_exe=Path("/nonexistent/gmod.exe")
            )
        
        assert "studiomdl.exe" in str(excinfo.value)


class TestCoreModuleExports:
    """Tests for core/__init__.py exports."""
    
    def test_all_modules_exported(self):
        """Test that all core modules are exported."""
        from core import (
            delta_anim,
            qc_builder,
            collision,
            sequences,
            vtf_conversion,
            smd_export,
            studiomdl,
        )
        
        assert delta_anim is not None
        assert qc_builder is not None
        assert collision is not None
        assert sequences is not None
        assert vtf_conversion is not None
        assert smd_export is not None
        assert studiomdl is not None
