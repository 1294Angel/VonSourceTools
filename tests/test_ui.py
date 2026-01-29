"""
Unit tests for the UI module.
These test panel class definitions and structure.
"""
import pytest
from pathlib import Path
import sys
from unittest.mock import MagicMock, patch

# Add the refactor directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "refactor"))


class TestUIModuleStructure:
    """Tests for UI module structure."""
    
    def test_ui_init_has_modules(self, mock_bpy):
        """Test that UI __init__ defines MODULES."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Panel = type('Panel', (), {})
            mock_bpy.types.UIList = type('UIList', (), {})
            
            from ui import MODULES
            
            assert isinstance(MODULES, list)
            assert len(MODULES) == 6  # parent, qc, delta_anim, vmt_generator, image_converter, smd_export
    
    def test_ui_has_register_functions(self, mock_bpy):
        """Test that UI module has register/unregister."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Panel = type('Panel', (), {})
            mock_bpy.types.UIList = type('UIList', (), {})
            
            from ui import register, unregister
            
            assert callable(register)
            assert callable(unregister)


class TestParentPanel:
    """Tests for parent_panel.py"""
    
    def test_parent_panel_defined(self, mock_bpy):
        """Test that parent panel is defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Panel = type('Panel', (), {})
            
            from ui.parent_panel import VON_PT_parent
            
            assert VON_PT_parent is not None
            assert VON_PT_parent.bl_idname == "VON_PT_parent"
            assert VON_PT_parent.bl_label == "Von Source Tools"
    
    def test_parent_panel_has_no_parent(self, mock_bpy):
        """Test that parent panel doesn't reference a parent."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Panel = type('Panel', (), {})
            
            from ui.parent_panel import VON_PT_parent
            
            assert not hasattr(VON_PT_parent, 'bl_parent_id')
    
    def test_parent_panel_classes_list(self, mock_bpy):
        """Test that CLASSES list is defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Panel = type('Panel', (), {})
            
            from ui.parent_panel import CLASSES
            
            assert len(CLASSES) == 1


class TestQCPanels:
    """Tests for qc_panels.py"""
    
    def test_qc_main_panel_defined(self, mock_bpy):
        """Test that QC main panel is defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Panel = type('Panel', (), {})
            
            from ui.qc_panels import VON_PT_qc_generator_main
            
            assert VON_PT_qc_generator_main is not None
            assert VON_PT_qc_generator_main.bl_parent_id == "VON_PT_parent"
    
    def test_qc_panels_count(self, mock_bpy):
        """Test that all QC panels are defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Panel = type('Panel', (), {})
            
            from ui.qc_panels import CLASSES
            
            assert len(CLASSES) == 5  # main, bodygroups, materials, animations, advanced
    
    def test_qc_subpanels_have_correct_parent(self, mock_bpy):
        """Test that QC subpanels reference correct parent."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Panel = type('Panel', (), {})
            
            from ui.qc_panels import (
                VON_PT_qc_bodygroups,
                VON_PT_qc_materials,
                VON_PT_qc_animations,
                VON_PT_qc_advanced,
            )
            
            assert VON_PT_qc_bodygroups.bl_parent_id == "VON_PT_qc_generator_main"
            assert VON_PT_qc_materials.bl_parent_id == "VON_PT_qc_generator_main"
            assert VON_PT_qc_animations.bl_parent_id == "VON_PT_qc_generator_main"
            assert VON_PT_qc_advanced.bl_parent_id == "VON_PT_qc_generator_main"


class TestDeltaAnimPanels:
    """Tests for delta_anim_panels.py"""
    
    def test_delta_anim_main_panel_defined(self, mock_bpy):
        """Test that delta animation main panel is defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Panel = type('Panel', (), {})
            
            from ui.delta_anim_panels import VON_PT_delta_animations
            
            assert VON_PT_delta_animations is not None
            assert VON_PT_delta_animations.bl_parent_id == "VON_PT_parent"
    
    def test_delta_anim_panels_count(self, mock_bpy):
        """Test that all delta anim panels are defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Panel = type('Panel', (), {})
            
            from ui.delta_anim_panels import CLASSES
            
            assert len(CLASSES) == 2  # main and advanced


class TestVMTGeneratorPanels:
    """Tests for vmt_generator_panels.py"""
    
    def test_material_list_defined(self, mock_bpy):
        """Test that material list UI is defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Panel = type('Panel', (), {})
            mock_bpy.types.UIList = type('UIList', (), {})
            
            from ui.vmt_generator_panels import VON_UL_MaterialList
            
            assert VON_UL_MaterialList is not None
    
    def test_vmt_generator_panel_defined(self, mock_bpy):
        """Test that VMT generator panel is defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Panel = type('Panel', (), {})
            mock_bpy.types.UIList = type('UIList', (), {})
            
            from ui.vmt_generator_panels import VON_PT_vmt_generator
            
            assert VON_PT_vmt_generator is not None
            assert VON_PT_vmt_generator.bl_parent_id == "VON_PT_parent"
    
    def test_vmt_material_settings_panel_defined(self, mock_bpy):
        """Test that VMT material settings panel is defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Panel = type('Panel', (), {})
            mock_bpy.types.UIList = type('UIList', (), {})
            
            from ui.vmt_generator_panels import VON_PT_vmt_material_settings
            
            assert VON_PT_vmt_material_settings is not None
            assert VON_PT_vmt_material_settings.bl_parent_id == "VON_PT_vmt_generator"
    
    def test_vmt_panels_count(self, mock_bpy):
        """Test that all VMT panels are defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Panel = type('Panel', (), {})
            mock_bpy.types.UIList = type('UIList', (), {})
            
            from ui.vmt_generator_panels import CLASSES
            
            assert len(CLASSES) == 3  # UIList, main panel, material settings


class TestImageConverterPanel:
    """Tests for image_converter_panel.py"""
    
    def test_image_converter_panel_defined(self, mock_bpy):
        """Test that image converter panel is defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Panel = type('Panel', (), {})
            
            from ui.image_converter_panel import VON_PT_image_converter
            
            assert VON_PT_image_converter is not None
            assert VON_PT_image_converter.bl_parent_id == "VON_PT_parent"
    
    def test_image_converter_classes_list(self, mock_bpy):
        """Test that CLASSES list is defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Panel = type('Panel', (), {})
            
            from ui.image_converter_panel import CLASSES
            
            assert len(CLASSES) == 1


class TestSMDExportPanel:
    """Tests for smd_export_panel.py"""
    
    def test_smd_export_panel_defined(self, mock_bpy):
        """Test that SMD export panel is defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Panel = type('Panel', (), {})
            
            from ui.smd_export_panel import VON_PT_smd_export
            
            assert VON_PT_smd_export is not None
            assert VON_PT_smd_export.bl_parent_id == "VON_PT_parent"
    
    def test_smd_export_classes_list(self, mock_bpy):
        """Test that CLASSES list is defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Panel = type('Panel', (), {})
            
            from ui.smd_export_panel import CLASSES
            
            assert len(CLASSES) == 1


class TestPanelNamingConventions:
    """Tests for panel naming conventions across all modules."""
    
    def test_all_panels_follow_naming_convention(self, mock_bpy):
        """Test that all panel bl_idnames follow VON_PT_ convention."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Panel = type('Panel', (), {})
            mock_bpy.types.UIList = type('UIList', (), {})
            
            from ui.parent_panel import CLASSES as parent_classes
            from ui.qc_panels import CLASSES as qc_classes
            from ui.delta_anim_panels import CLASSES as delta_classes
            from ui.vmt_generator_panels import CLASSES as vmt_classes
            from ui.image_converter_panel import CLASSES as image_classes
            from ui.smd_export_panel import CLASSES as smd_classes
            
            all_classes = (
                parent_classes + qc_classes + delta_classes + 
                vmt_classes + image_classes + smd_classes
            )
            
            for cls in all_classes:
                if hasattr(cls, 'bl_idname'):
                    # Panels should start with VON_PT_, UILists with VON_UL_
                    assert (cls.bl_idname.startswith('VON_PT_') or 
                            cls.bl_idname.startswith('VON_UL_')), \
                        f"{cls.__name__} has invalid bl_idname: {cls.bl_idname}"
    
    def test_all_panels_in_vonsourcetools_category(self, mock_bpy):
        """Test that all panels are in VonSourceTools category."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Panel = type('Panel', (), {})
            mock_bpy.types.UIList = type('UIList', (), {})
            
            from ui.parent_panel import CLASSES as parent_classes
            from ui.qc_panels import CLASSES as qc_classes
            from ui.delta_anim_panels import CLASSES as delta_classes
            from ui.vmt_generator_panels import CLASSES as vmt_classes
            from ui.image_converter_panel import CLASSES as image_classes
            from ui.smd_export_panel import CLASSES as smd_classes
            
            all_classes = (
                parent_classes + qc_classes + delta_classes + 
                vmt_classes + image_classes + smd_classes
            )
            
            for cls in all_classes:
                if hasattr(cls, 'bl_category'):
                    assert cls.bl_category == 'VonSourceTools', \
                        f"{cls.__name__} not in VonSourceTools category"


class TestTotalPanelCount:
    """Tests for expected total panel count."""
    
    def test_total_panel_count(self, mock_bpy):
        """Test that expected total number of panels are defined."""
        with patch.dict(sys.modules, {'bpy': mock_bpy}):
            mock_bpy.types.Panel = type('Panel', (), {})
            mock_bpy.types.UIList = type('UIList', (), {})
            
            from ui.parent_panel import CLASSES as parent_classes
            from ui.qc_panels import CLASSES as qc_classes
            from ui.delta_anim_panels import CLASSES as delta_classes
            from ui.vmt_generator_panels import CLASSES as vmt_classes
            from ui.image_converter_panel import CLASSES as image_classes
            from ui.smd_export_panel import CLASSES as smd_classes
            
            total = (len(parent_classes) + len(qc_classes) + len(delta_classes) + 
                     len(vmt_classes) + len(image_classes) + len(smd_classes))
            
            # Expected: 1 + 5 + 2 + 3 + 1 + 1 = 13
            assert total == 13, f"Expected 13 UI classes, got {total}"
