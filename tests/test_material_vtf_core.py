"""
Unit tests for the material_vtf core module.
"""
import pytest
from pathlib import Path
import sys
import os
import tempfile
from unittest.mock import MagicMock, patch

# Add the refactor directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "refactor"))


class TestGetMaterialsRelativePath:
    """Tests for get_materials_relative_path function."""
    
    def test_extracts_path_after_materials(self):
        """Test extraction of path after materials folder."""
        from core.material_vtf import get_materials_relative_path
        
        test_path = "/game/garrysmod/materials/models/player/test"
        result = get_materials_relative_path(test_path)
        
        assert result == "models/player/test"
    
    def test_handles_windows_paths(self):
        """Test handling of Windows-style paths."""
        from core.material_vtf import get_materials_relative_path
        
        test_path = "C:\\game\\garrysmod\\materials\\models\\player\\test"
        result = get_materials_relative_path(test_path)
        
        assert result == "models/player/test"
    
    def test_returns_empty_for_no_materials_folder(self):
        """Test returns empty string when no materials folder."""
        from core.material_vtf import get_materials_relative_path
        
        test_path = "/game/garrysmod/models/player/test"
        result = get_materials_relative_path(test_path)
        
        assert result == ""
    
    def test_handles_trailing_slash(self):
        """Test handling of trailing slashes."""
        from core.material_vtf import get_materials_relative_path
        
        test_path = "/game/garrysmod/materials/models/player/"
        result = get_materials_relative_path(test_path)
        
        assert result == "models/player"
    
    def test_case_insensitive(self):
        """Test that Materials folder detection is case insensitive."""
        from core.material_vtf import get_materials_relative_path
        
        test_path = "/game/garrysmod/MATERIALS/models/player"
        result = get_materials_relative_path(test_path)
        
        assert result == "models/player"


class TestGenerateVMTContent:
    """Tests for generate_vmt_content function."""
    
    def test_generates_basic_vmt(self, mock_bpy):
        """Test generation of basic VMT content."""
        from core.material_vtf import generate_vmt_content
        
        # Create mock vmt_params
        vmt_params = MagicMock()
        vmt_params.enable_phong = False
        vmt_params.enable_rimlight = False
        vmt_params.enable_envmap = False
        vmt_params.normal_map = None
        vmt_params.phong_exponent_map = None
        vmt_params.color2 = (0.0, 0.0, 0.0)
        vmt_params.blend_tint_by_base_alpha = True
        vmt_params.normal_map_alpha_envmap_mask = False
        
        result = generate_vmt_content(
            material_name="test_material",
            vmt_params=vmt_params,
            shader_type="VertexlitGeneric",
            base_texture_path="test_material"
        )
        
        assert '"VertexlitGeneric"' in result
        assert '"$basetexture"' in result
        assert 'test_material' in result
    
    def test_includes_phong_when_enabled(self, mock_bpy):
        """Test that phong parameters are included when enabled."""
        from core.material_vtf import generate_vmt_content
        
        vmt_params = MagicMock()
        vmt_params.enable_phong = True
        vmt_params.phong_boost = 1.5
        vmt_params.phong_albedo_tint = True
        vmt_params.phong_albedo_boost = 50.0
        vmt_params.phong_fresnel_ranges = (1.0, 0.1, 0.0)
        vmt_params.enable_rimlight = False
        vmt_params.enable_envmap = False
        vmt_params.normal_map = None
        vmt_params.phong_exponent_map = None
        vmt_params.color2 = (0.0, 0.0, 0.0)
        vmt_params.blend_tint_by_base_alpha = True
        vmt_params.normal_map_alpha_envmap_mask = False
        
        result = generate_vmt_content(
            material_name="test",
            vmt_params=vmt_params,
            shader_type="VertexlitGeneric",
            base_texture_path="test"
        )
        
        assert '"$phong" "1"' in result
        assert '"$phongboost"' in result
        assert '"$phongalbedotint"' in result
    
    def test_includes_rimlight_when_enabled(self, mock_bpy):
        """Test that rim lighting parameters are included when enabled."""
        from core.material_vtf import generate_vmt_content
        
        vmt_params = MagicMock()
        vmt_params.enable_phong = False
        vmt_params.enable_rimlight = True
        vmt_params.rimlight_exponent = 100.0
        vmt_params.rimlight_boost = 1.0
        vmt_params.rim_mask = True
        vmt_params.enable_envmap = False
        vmt_params.normal_map = None
        vmt_params.phong_exponent_map = None
        vmt_params.color2 = (0.0, 0.0, 0.0)
        vmt_params.blend_tint_by_base_alpha = True
        vmt_params.normal_map_alpha_envmap_mask = False
        
        result = generate_vmt_content(
            material_name="test",
            vmt_params=vmt_params,
            shader_type="VertexlitGeneric",
            base_texture_path="test"
        )
        
        assert '"$rimlight" "1"' in result
        assert '"$rimlightexponent"' in result
        assert '"$rimmask"' in result
    
    def test_includes_envmap_when_enabled(self, mock_bpy):
        """Test that environment mapping is included when enabled."""
        from core.material_vtf import generate_vmt_content
        
        vmt_params = MagicMock()
        vmt_params.enable_phong = False
        vmt_params.enable_rimlight = False
        vmt_params.enable_envmap = True
        vmt_params.envmap_tint = (0.11, 0.106, 0.106)
        vmt_params.normal_map = None
        vmt_params.phong_exponent_map = None
        vmt_params.color2 = (0.0, 0.0, 0.0)
        vmt_params.blend_tint_by_base_alpha = True
        vmt_params.normal_map_alpha_envmap_mask = False
        
        result = generate_vmt_content(
            material_name="test",
            vmt_params=vmt_params,
            shader_type="VertexlitGeneric",
            base_texture_path="test"
        )
        
        assert '"$envmap"' in result
        assert '"$envmaptint"' in result
    
    def test_includes_normal_map_when_provided(self, mock_bpy):
        """Test that normal map is included when provided."""
        from core.material_vtf import generate_vmt_content
        
        vmt_params = MagicMock()
        vmt_params.enable_phong = False
        vmt_params.enable_rimlight = False
        vmt_params.enable_envmap = False
        vmt_params.normal_map = MagicMock()  # Non-None normal map
        vmt_params.phong_exponent_map = None
        vmt_params.color2 = (0.0, 0.0, 0.0)
        vmt_params.blend_tint_by_base_alpha = True
        vmt_params.normal_map_alpha_envmap_mask = False
        
        result = generate_vmt_content(
            material_name="test",
            vmt_params=vmt_params,
            shader_type="VertexlitGeneric",
            base_texture_path="test",
            normal_texture_path="test_n"
        )
        
        assert '"$bumpmap"' in result
        assert 'test_n' in result
    
    def test_includes_global_params(self, mock_bpy):
        """Test that global parameters are included."""
        from core.material_vtf import generate_vmt_content
        
        vmt_params = MagicMock()
        vmt_params.enable_phong = False
        vmt_params.enable_rimlight = False
        vmt_params.enable_envmap = False
        vmt_params.normal_map = None
        vmt_params.phong_exponent_map = None
        vmt_params.color2 = (0.0, 0.0, 0.0)
        vmt_params.blend_tint_by_base_alpha = True
        vmt_params.normal_map_alpha_envmap_mask = False
        
        global_params = {
            'additive': True,
            'translucent': True,
            'nocull': True
        }
        
        result = generate_vmt_content(
            material_name="test",
            vmt_params=vmt_params,
            shader_type="VertexlitGeneric",
            base_texture_path="test",
            global_params=global_params
        )
        
        assert '"$additive" "1"' in result
        assert '"$translucent" "1"' in result
        assert '"$nocull" "1"' in result


class TestWriteVMTFile:
    """Tests for write_vmt_file function."""
    
    def test_writes_file_to_disk(self):
        """Test that VMT file is written to disk."""
        from core.material_vtf import write_vmt_file
        
        with tempfile.TemporaryDirectory() as tmpdir:
            vmt_content = '"VertexlitGeneric"\n{\n    "$basetexture" "test"\n}\n'
            
            result = write_vmt_file(tmpdir, "test_material", vmt_content)
            
            assert os.path.exists(result)
            assert result.endswith(".vmt")
            
            with open(result, 'r') as f:
                content = f.read()
            
            assert content == vmt_content
    
    def test_returns_correct_filepath(self):
        """Test that correct filepath is returned."""
        from core.material_vtf import write_vmt_file
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = write_vmt_file(tmpdir, "my_material", "content")
            
            assert result == os.path.join(tmpdir, "my_material.vmt")


class TestBuildVTFCmdCommand:
    """Tests for build_vtfcmd_command function."""
    
    def test_raises_for_missing_vtfcmd(self):
        """Test that FileNotFoundError is raised for missing VTFCmd."""
        from core.material_vtf import build_vtfcmd_command
        
        with pytest.raises(FileNotFoundError) as excinfo:
            build_vtfcmd_command(
                vtfcmd_exe="/nonexistent/VTFCmd.exe",
                image_paths=[],
                image_name_mapping={},
                output_path="/tmp"
            )
        
        assert "VTFCmd.exe" in str(excinfo.value)
    
    def test_raises_for_missing_output_path(self):
        """Test that FileNotFoundError is raised for missing output path."""
        from core.material_vtf import build_vtfcmd_command
        
        # Create a temporary "VTFCmd.exe" file
        with tempfile.TemporaryDirectory() as tmpdir:
            vtfcmd_path = os.path.join(tmpdir, "VTFCmd.exe")
            with open(vtfcmd_path, 'w') as f:
                f.write("dummy")
            
            with pytest.raises(FileNotFoundError) as excinfo:
                build_vtfcmd_command(
                    vtfcmd_exe=vtfcmd_path,
                    image_paths=[],
                    image_name_mapping={},
                    output_path="/nonexistent/output"
                )
            
            assert "output" in str(excinfo.value).lower()
    
    def test_includes_format_parameters(self):
        """Test that format parameters are included in command."""
        from core.material_vtf import build_vtfcmd_command
        
        with tempfile.TemporaryDirectory() as tmpdir:
            vtfcmd_path = os.path.join(tmpdir, "VTFCmd.exe")
            with open(vtfcmd_path, 'w') as f:
                f.write("dummy")
            
            output_path = os.path.join(tmpdir, "output")
            os.makedirs(output_path)
            
            result = build_vtfcmd_command(
                vtfcmd_exe=vtfcmd_path,
                image_paths=[],
                image_name_mapping={},
                output_path=output_path,
                vtf_format='dxt5',
                alpha_format='dxt5',
                vtf_version='7.5'
            )
            
            assert "-format" in result
            assert "dxt5" in result
            assert "-alphaformat" in result
            assert "-version" in result
            assert "7.5" in result
    
    def test_includes_resize_parameters_when_enabled(self):
        """Test that resize parameters are included when resize is enabled."""
        from core.material_vtf import build_vtfcmd_command
        
        with tempfile.TemporaryDirectory() as tmpdir:
            vtfcmd_path = os.path.join(tmpdir, "VTFCmd.exe")
            with open(vtfcmd_path, 'w') as f:
                f.write("dummy")
            
            output_path = os.path.join(tmpdir, "output")
            os.makedirs(output_path)
            
            result = build_vtfcmd_command(
                vtfcmd_exe=vtfcmd_path,
                image_paths=[],
                image_name_mapping={},
                output_path=output_path,
                resize=True,
                resize_method='BIGGEST',
                resize_filter='TRIANGLE',
                clamp_size='512x512'
            )
            
            assert "-resize" in result
            assert "-rmethod" in result
            assert "-rfilter" in result
            assert "-rclampwidth" in result
            assert "-rclampheight" in result


class TestCollectSceneMaterials:
    """Tests for collect_scene_materials function."""
    
    def test_returns_empty_for_empty_scene(self, mock_bpy):
        """Test that empty list is returned for scene with no objects."""
        from core.material_vtf import collect_scene_materials
        
        context = MagicMock()
        context.scene.objects = []
        
        result = collect_scene_materials(context)
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_collects_materials_from_objects(self, mock_bpy):
        """Test that materials are collected from scene objects."""
        from core.material_vtf import collect_scene_materials
        
        # Create mock material
        material = MagicMock()
        material.name = "TestMaterial"
        material.users = 1
        
        # Create mock material slot
        material_slot = MagicMock()
        material_slot.material = material
        
        # Create mock object
        obj = MagicMock()
        obj.material_slots = [material_slot]
        
        # Create mock context
        context = MagicMock()
        context.scene.objects = [obj]
        
        result = collect_scene_materials(context)
        
        assert len(result) == 1
        assert result[0].material.name == "TestMaterial"
    
    def test_deduplicates_materials(self, mock_bpy):
        """Test that duplicate materials are not included."""
        from core.material_vtf import collect_scene_materials
        
        # Create mock material
        material = MagicMock()
        material.name = "SharedMaterial"
        material.users = 2
        
        # Create mock material slots for two objects
        material_slot1 = MagicMock()
        material_slot1.material = material
        
        material_slot2 = MagicMock()
        material_slot2.material = material
        
        # Create mock objects
        obj1 = MagicMock()
        obj1.material_slots = [material_slot1]
        
        obj2 = MagicMock()
        obj2.material_slots = [material_slot2]
        
        context = MagicMock()
        context.scene.objects = [obj1, obj2]
        
        result = collect_scene_materials(context)
        
        # Should only have one material despite being on two objects
        assert len(result) == 1
    
    def test_skips_materials_with_no_users(self, mock_bpy):
        """Test that materials with no users are skipped."""
        from core.material_vtf import collect_scene_materials
        
        material = MagicMock()
        material.name = "UnusedMaterial"
        material.users = 0  # No users
        
        material_slot = MagicMock()
        material_slot.material = material
        
        obj = MagicMock()
        obj.material_slots = [material_slot]
        
        context = MagicMock()
        context.scene.objects = [obj]
        
        result = collect_scene_materials(context)
        
        assert len(result) == 0


class TestGetImageTextureNode:
    """Tests for get_image_texture_node function."""
    
    def test_returns_none_for_no_node_tree(self, mock_bpy):
        """Test that None is returned when material has no node tree."""
        from core.material_vtf import get_image_texture_node
        
        material = MagicMock()
        material.node_tree = None
        
        result = get_image_texture_node(material)
        
        assert result is None
    
    def test_returns_none_for_no_principled_bsdf(self, mock_bpy):
        """Test that None is returned when no Principled BSDF exists."""
        from core.material_vtf import get_image_texture_node
        
        material = MagicMock()
        material.node_tree = MagicMock()
        
        # Create a node that is NOT Principled BSDF
        node = MagicMock()
        node.type = 'DIFFUSE_BSDF'
        
        material.node_tree.nodes = [node]
        
        result = get_image_texture_node(material)
        
        assert result is None
    
    def test_returns_image_texture_node(self, mock_bpy):
        """Test that image texture node is returned when properly connected."""
        from core.material_vtf import get_image_texture_node
        
        # Create image texture node
        image_node = MagicMock()
        image_node.type = 'TEX_IMAGE'
        
        # Create link
        link = MagicMock()
        link.from_node = image_node
        
        # Create base color input
        base_color_input = MagicMock()
        base_color_input.is_linked = True
        base_color_input.links = [link]
        
        # Create Principled BSDF
        principled = MagicMock()
        principled.type = 'BSDF_PRINCIPLED'
        principled.inputs.get.return_value = base_color_input
        
        # Setup material
        material = MagicMock()
        material.node_tree.nodes = [principled, image_node]
        
        result = get_image_texture_node(material)
        
        assert result == image_node
