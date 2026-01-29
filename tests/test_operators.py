"""
Unit tests for the operators module.
These test operator class definitions and structure.
"""
import pytest
from pathlib import Path
import sys
from unittest.mock import MagicMock, patch

# Add the refactor directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "refactor"))


class TestOperatorStructure:
    """Tests for operator module structure."""
    
    def test_operators_init_has_modules(self, mock_bpy):
        """Test that operators __init__ defines MODULES."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators import MODULES
            
            assert isinstance(MODULES, list)
            assert len(MODULES) == 5  # delta_anim, qc, smd, vtf, studiomdl
    
    def test_operators_has_register_functions(self, mock_bpy):
        """Test that operators module has register/unregister."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators import register, unregister
            
            assert callable(register)
            assert callable(unregister)


class TestDeltaAnimOperators:
    """Tests for delta animation operators."""
    
    def test_delta_anim_operators_classes_exist(self, mock_bpy):
        """Test that delta animation operator classes are defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators import delta_anim_operators
            
            assert hasattr(delta_anim_operators, 'CLASSES')
            assert len(delta_anim_operators.CLASSES) > 0
    
    def test_delta_anim_full_operator_defined(self, mock_bpy):
        """Test that the full delta anim operator is defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.delta_anim_operators import VONANIM_OT_full
            
            assert VONANIM_OT_full is not None
            assert hasattr(VONANIM_OT_full, 'bl_idname')
            assert VONANIM_OT_full.bl_idname == "von.deltaanimtrick_full"
    
    def test_delta_anim_operator_has_poll(self, mock_bpy):
        """Test that delta anim full operator has poll method."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.delta_anim_operators import VONANIM_OT_full
            
            assert hasattr(VONANIM_OT_full, 'poll')
            assert callable(VONANIM_OT_full.poll)


class TestQCOperators:
    """Tests for QC generation operators."""
    
    def test_qc_operators_classes_exist(self, mock_bpy):
        """Test that QC operator classes are defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators import qc_operators
            
            assert hasattr(qc_operators, 'CLASSES')
            assert len(qc_operators.CLASSES) > 0
    
    def test_qc_generate_operators_defined(self, mock_bpy):
        """Test that all QC generation operators are defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.qc_operators import (
                VONQC_OT_generate_prop,
                VONQC_OT_generate_character,
                VONQC_OT_generate_npc,
            )
            
            assert VONQC_OT_generate_prop is not None
            assert VONQC_OT_generate_character is not None
            assert VONQC_OT_generate_npc is not None
    
    def test_collect_sequences_operator_defined(self, mock_bpy):
        """Test that collect sequences operator is defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.qc_operators import VONQC_OT_collect_sequences
            
            assert VONQC_OT_collect_sequences is not None
            assert hasattr(VONQC_OT_collect_sequences, 'bl_idname')
            assert VONQC_OT_collect_sequences.bl_idname == "von.collect_sequences"


class TestSMDOperators:
    """Tests for SMD export operators."""
    
    def test_smd_operators_classes_exist(self, mock_bpy):
        """Test that SMD operator classes are defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators import smd_operators
            
            assert hasattr(smd_operators, 'CLASSES')
            assert len(smd_operators.CLASSES) == 3
    
    def test_split_restore_operators_defined(self, mock_bpy):
        """Test that split and restore operators are defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.smd_operators import (
                VONSMD_OT_split_objects,
                VONSMD_OT_restore_objects,
            )
            
            assert VONSMD_OT_split_objects.bl_idname == "object.split_objects"
            assert VONSMD_OT_restore_objects.bl_idname == "object.restore_objects"


class TestVTFOperators:
    """Tests for VTF conversion operators."""
    
    def test_vtf_operators_classes_exist(self, mock_bpy):
        """Test that VTF operator classes are defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators import vtf_operators
            
            assert hasattr(vtf_operators, 'CLASSES')
            assert len(vtf_operators.CLASSES) == 1
    
    def test_batch_convert_operator_defined(self, mock_bpy):
        """Test that batch convert operator is defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.vtf_operators import VONVTF_OT_batch_convert
            
            assert VONVTF_OT_batch_convert.bl_idname == "von.batchconvertfiletypes"


class TestStudioMDLOperators:
    """Tests for StudioMDL operators."""
    
    def test_studiomdl_operators_classes_exist(self, mock_bpy):
        """Test that StudioMDL operator classes are defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators import studiomdl_operators
            
            assert hasattr(studiomdl_operators, 'CLASSES')
            assert len(studiomdl_operators.CLASSES) == 1
    
    def test_definebones_operator_defined(self, mock_bpy):
        """Test that definebones operator is defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators.studiomdl_operators import VONSTUDIOMDL_OT_run_definebones
            
            assert VONSTUDIOMDL_OT_run_definebones.bl_idname == "von.run_definebones_vondata"


class TestOperatorNamingConventions:
    """Tests for operator naming conventions."""
    
    def test_all_operators_have_bl_idname(self, mock_bpy):
        """Test that all operators have bl_idname."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators import (
                delta_anim_operators,
                qc_operators,
                smd_operators,
                vtf_operators,
                studiomdl_operators,
            )
            
            all_classes = (
                delta_anim_operators.CLASSES +
                qc_operators.CLASSES +
                smd_operators.CLASSES +
                vtf_operators.CLASSES +
                studiomdl_operators.CLASSES
            )
            
            for cls in all_classes:
                assert hasattr(cls, 'bl_idname'), f"{cls.__name__} missing bl_idname"
                assert hasattr(cls, 'bl_label'), f"{cls.__name__} missing bl_label"
    
    def test_all_operators_have_execute(self, mock_bpy):
        """Test that all operators have execute method."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Operator = type('Operator', (), {})
            
            from operators import (
                delta_anim_operators,
                qc_operators,
                smd_operators,
                vtf_operators,
                studiomdl_operators,
            )
            
            all_classes = (
                delta_anim_operators.CLASSES +
                qc_operators.CLASSES +
                smd_operators.CLASSES +
                vtf_operators.CLASSES +
                studiomdl_operators.CLASSES
            )
            
            for cls in all_classes:
                assert hasattr(cls, 'execute'), f"{cls.__name__} missing execute method"
