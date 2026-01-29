"""
Unit tests for the material_vtf_operators module.
"""
import pytest
from pathlib import Path
import sys
from unittest.mock import MagicMock, patch

# Add the refactor directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "refactor"))


class TestRefreshMaterialsOperator:
    """Tests for VONVTF_OT_refresh_materials operator."""
    
    def test_operator_class_exists(self, mock_bpy):
        """Test that the refresh materials operator class exists."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.material_vtf_operators import VONVTF_OT_refresh_materials
            
            assert VONVTF_OT_refresh_materials is not None
    
    def test_operator_has_correct_bl_idname(self, mock_bpy):
        """Test that operator has correct bl_idname."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.material_vtf_operators import VONVTF_OT_refresh_materials
            
            assert VONVTF_OT_refresh_materials.bl_idname == "von.vtf_refresh_materials"
    
    def test_operator_has_poll_method(self, mock_bpy):
        """Test that operator has poll method."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.material_vtf_operators import VONVTF_OT_refresh_materials
            
            assert hasattr(VONVTF_OT_refresh_materials, 'poll')
            assert callable(VONVTF_OT_refresh_materials.poll)
    
    def test_operator_has_execute_method(self, mock_bpy):
        """Test that operator has execute method."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.material_vtf_operators import VONVTF_OT_refresh_materials
            
            assert hasattr(VONVTF_OT_refresh_materials, 'execute')


class TestConvertMaterialsOperator:
    """Tests for VONVTF_OT_convert_materials operator."""
    
    def test_operator_class_exists(self, mock_bpy):
        """Test that the convert materials operator class exists."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.material_vtf_operators import VONVTF_OT_convert_materials
            
            assert VONVTF_OT_convert_materials is not None
    
    def test_operator_has_correct_bl_idname(self, mock_bpy):
        """Test that operator has correct bl_idname."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.material_vtf_operators import VONVTF_OT_convert_materials
            
            assert VONVTF_OT_convert_materials.bl_idname == "von.vtf_convert_materials"
    
    def test_operator_has_poll_method(self, mock_bpy):
        """Test that operator has poll method."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.material_vtf_operators import VONVTF_OT_convert_materials
            
            assert hasattr(VONVTF_OT_convert_materials, 'poll')
            assert callable(VONVTF_OT_convert_materials.poll)
    
    def test_operator_has_execute_method(self, mock_bpy):
        """Test that operator has execute method."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.material_vtf_operators import VONVTF_OT_convert_materials
            
            assert hasattr(VONVTF_OT_convert_materials, 'execute')
    
    def test_operator_has_generate_vmt_files_method(self, mock_bpy):
        """Test that operator has _generate_vmt_files method."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.material_vtf_operators import VONVTF_OT_convert_materials
            
            assert hasattr(VONVTF_OT_convert_materials, '_generate_vmt_files')


class TestSelectAllMaterialsOperator:
    """Tests for VONVTF_OT_select_all_materials operator."""
    
    def test_operator_class_exists(self, mock_bpy):
        """Test that the select all operator class exists."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.material_vtf_operators import VONVTF_OT_select_all_materials
            
            assert VONVTF_OT_select_all_materials is not None
    
    def test_operator_has_correct_bl_idname(self, mock_bpy):
        """Test that operator has correct bl_idname."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.material_vtf_operators import VONVTF_OT_select_all_materials
            
            assert VONVTF_OT_select_all_materials.bl_idname == "von.vtf_select_all"


class TestDeselectAllMaterialsOperator:
    """Tests for VONVTF_OT_deselect_all_materials operator."""
    
    def test_operator_class_exists(self, mock_bpy):
        """Test that the deselect all operator class exists."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.material_vtf_operators import VONVTF_OT_deselect_all_materials
            
            assert VONVTF_OT_deselect_all_materials is not None
    
    def test_operator_has_correct_bl_idname(self, mock_bpy):
        """Test that operator has correct bl_idname."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.material_vtf_operators import VONVTF_OT_deselect_all_materials
            
            assert VONVTF_OT_deselect_all_materials.bl_idname == "von.vtf_deselect_all"


class TestMaterialVTFOperatorsModule:
    """Tests for material_vtf_operators module structure."""
    
    def test_classes_list_defined(self, mock_bpy):
        """Test that CLASSES list is defined with all operators."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.material_vtf_operators import CLASSES
            
            assert isinstance(CLASSES, list)
            assert len(CLASSES) == 4
    
    def test_register_function_exists(self, mock_bpy):
        """Test that register function is defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.material_vtf_operators import register, unregister
            
            assert callable(register)
            assert callable(unregister)
    
    def test_all_operators_have_required_attributes(self, mock_bpy):
        """Test that all operators have required Blender attributes."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.material_vtf_operators import CLASSES
            
            required_attrs = ['bl_idname', 'bl_label', 'bl_description']
            
            for cls in CLASSES:
                for attr in required_attrs:
                    assert hasattr(cls, attr), f"{cls.__name__} missing {attr}"
    
    def test_all_operators_have_options(self, mock_bpy):
        """Test that all operators have bl_options defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.material_vtf_operators import CLASSES
            
            for cls in CLASSES:
                assert hasattr(cls, 'bl_options'), f"{cls.__name__} missing bl_options"
