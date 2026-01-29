"""
Unit tests for the QC builder module.
"""
import pytest
from pathlib import Path
import sys
import os
import tempfile
from unittest.mock import MagicMock, patch

# Add the refactor directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "refactor"))


class TestQCDataClass:
    """Tests for QCData dataclass."""
    
    def test_qcdata_default_values(self):
        """Test QCData has correct default values."""
        from core.qc_builder import QCData
        
        qc_data = QCData()
        
        assert qc_data.model_type == "PROP"
        assert qc_data.model_name == ""
        assert qc_data.scale == 1
        assert qc_data.staticprop == False
        assert qc_data.material_paths == []
        assert qc_data.bodygroups == {}
        assert qc_data.sequences == []
    
    def test_qcdata_custom_values(self):
        """Test QCData with custom values."""
        from core.qc_builder import QCData
        
        qc_data = QCData(
            model_type="CHARACTER",
            model_name="test_model",
            scale=2,
            material_paths=["models/test"],
            staticprop=False
        )
        
        assert qc_data.model_type == "CHARACTER"
        assert qc_data.model_name == "test_model"
        assert qc_data.scale == 2
        assert qc_data.material_paths == ["models/test"]


class TestTemplateLoading:
    """Tests for template loading functions."""
    
    def test_load_template_modelname(self):
        """Test loading modelname template."""
        from core.qc_builder import load_template
        
        template = load_template("modelname")
        
        assert "$modelname" in template
        assert "{mdlModelName}" in template
    
    def test_load_template_bodygroup(self):
        """Test loading bodygroup template."""
        from core.qc_builder import load_template
        
        template = load_template("bodygroup")
        
        assert "$bodygroup" in template
        assert "{bodygroupName}" in template
        assert "{bodygroupLines}" in template
    
    def test_load_template_sequence(self):
        """Test loading sequence template."""
        from core.qc_builder import load_template
        
        template = load_template("sequence")
        
        assert "$sequence" in template
        assert "{sequenceName}" in template
        assert "{sequenceFile}" in template
        assert "{fps}" in template
    
    def test_load_template_not_found(self):
        """Test that FileNotFoundError is raised for missing template."""
        from core.qc_builder import load_template
        
        with pytest.raises(FileNotFoundError):
            load_template("nonexistent_template")
    
    def test_load_section_order(self):
        """Test loading section order configuration."""
        from core.qc_builder import load_section_order
        
        config = load_section_order("PROP")
        
        assert "sections" in config
        assert "flags" in config
        assert "modelname" in config["sections"]
        assert "staticprop" in config["flags"]
    
    def test_load_section_order_character(self):
        """Test loading section order for character model type."""
        from core.qc_builder import load_section_order
        
        config = load_section_order("CHARACTER")
        
        assert "sections" in config
        assert "modelname" in config["sections"]
        assert "sequence" in config["sections"]
    
    def test_load_section_order_invalid_type(self):
        """Test that ValueError is raised for invalid model type."""
        from core.qc_builder import load_section_order
        
        with pytest.raises(ValueError):
            load_section_order("INVALID_TYPE")


class TestSectionGenerators:
    """Tests for individual section generator functions."""
    
    def test_generate_modelname(self):
        """Test generating modelname section."""
        from core.qc_builder import QCData, generate_modelname
        
        qc_data = QCData(model_name="test_model")
        result = generate_modelname(qc_data)
        
        assert '$modelname "test_model.mdl"' in result
    
    def test_generate_modelname_empty(self):
        """Test that empty string returned for empty model name."""
        from core.qc_builder import QCData, generate_modelname
        
        qc_data = QCData(model_name="")
        result = generate_modelname(qc_data)
        
        assert result == ""
    
    def test_generate_scale(self):
        """Test generating scale section."""
        from core.qc_builder import QCData, generate_scale
        
        qc_data = QCData(scale=2)
        result = generate_scale(qc_data)
        
        assert "$scale 2" in result
    
    def test_generate_scale_default(self):
        """Test that empty string returned for default scale."""
        from core.qc_builder import QCData, generate_scale
        
        qc_data = QCData(scale=1)
        result = generate_scale(qc_data)
        
        assert result == ""
    
    def test_generate_surfaceprop(self):
        """Test generating surfaceprop section."""
        from core.qc_builder import QCData, generate_surfaceprop
        
        qc_data = QCData(surfaceprop="metal")
        result = generate_surfaceprop(qc_data)
        
        assert '$surfaceprop "metal"' in result
    
    def test_generate_cdmaterials_single(self):
        """Test generating cdmaterials with single path."""
        from core.qc_builder import QCData, generate_cdmaterials
        
        qc_data = QCData(material_paths=["models/test"])
        result = generate_cdmaterials(qc_data)
        
        assert '$cdmaterials "models/test"' in result
    
    def test_generate_cdmaterials_multiple(self):
        """Test generating cdmaterials with multiple paths."""
        from core.qc_builder import QCData, generate_cdmaterials
        
        qc_data = QCData(material_paths=["models/test1", "models/test2"])
        result = generate_cdmaterials(qc_data)
        
        assert '$cdmaterials "models/test1"' in result
        assert '$cdmaterials "models/test2"' in result
    
    def test_generate_bodygroups(self):
        """Test generating bodygroup section."""
        from core.qc_builder import QCData, generate_bodygroups
        
        qc_data = QCData(bodygroups={"body": ["mesh1", "mesh2"]})
        result = generate_bodygroups(qc_data)
        
        assert '$bodygroup "body"' in result
        assert 'studio "mesh1.smd"' in result
        assert 'studio "mesh2.smd"' in result
        assert 'blank' in result
    
    def test_generate_sequences(self):
        """Test generating sequence section."""
        from core.qc_builder import QCData, generate_sequences
        
        qc_data = QCData(sequences=[
            {"name": "idle", "file": "idle", "fps": 30}
        ])
        result = generate_sequences(qc_data)
        
        assert '$sequence "idle"' in result
        assert '"idle.smd"' in result
        assert 'fps 30' in result
    
    def test_generate_sequences_with_activity(self):
        """Test generating sequence with activity."""
        from core.qc_builder import QCData, generate_sequences
        
        qc_data = QCData(sequences=[
            {"name": "walk", "file": "walk", "fps": 30, "activity": "ACT_WALK", "activity_weight": 1}
        ])
        result = generate_sequences(qc_data)
        
        assert 'activity "ACT_WALK"' in result
    
    def test_generate_sequences_default_for_prop(self):
        """Test default idle sequence for props."""
        from core.qc_builder import QCData, generate_sequences
        
        qc_data = QCData(model_type="PROP", sequences=[])
        result = generate_sequences(qc_data)
        
        assert '$sequence "idle"' in result
    
    def test_generate_collisionmodel(self):
        """Test generating collisionmodel section."""
        from core.qc_builder import QCData, generate_collisionmodel
        
        qc_data = QCData(
            model_name="test",
            generate_collision=True,
            collision_mass=100.0
        )
        result = generate_collisionmodel(qc_data)
        
        assert '$collisionmodel "test_phys.smd"' in result
        assert '$mass 100' in result
    
    def test_generate_collisionmodel_with_collection(self):
        """Test generating collisionmodel with existing collection."""
        from core.qc_builder import QCData, generate_collisionmodel
        
        qc_data = QCData(
            generate_collision=False,
            collision_collection="phys_mesh",
            collision_mass=50.0
        )
        result = generate_collisionmodel(qc_data)
        
        assert '$collisionmodel "phys_mesh.smd"' in result
    
    def test_generate_staticprop(self):
        """Test generating staticprop flag."""
        from core.qc_builder import QCData, generate_staticprop
        
        qc_data = QCData(staticprop=True)
        result = generate_staticprop(qc_data)
        
        assert result == "$staticprop"
    
    def test_generate_includemodel(self):
        """Test generating includemodel command."""
        from core.qc_builder import QCData, generate_includemodel
        
        qc_data = QCData(include_default_anims="m_anm.mdl")
        result = generate_includemodel(qc_data)
        
        assert '$includemodel "m_anm.mdl"' in result


class TestQCContentBuilding:
    """Tests for building complete QC content."""
    
    def test_build_qc_content_prop(self):
        """Test building complete QC content for prop."""
        from core.qc_builder import QCData, build_qc_content
        
        qc_data = QCData(
            model_type="PROP",
            model_name="test_prop",
            material_paths=["models/props"],
            surfaceprop="metal",
            staticprop=True
        )
        
        content = build_qc_content(qc_data)
        
        assert "// QC file generated by VonSourceTools" in content
        assert '$modelname "test_prop.mdl"' in content
        assert '$cdmaterials "models/props"' in content
        assert '$surfaceprop "metal"' in content
        assert "$staticprop" in content
    
    def test_build_qc_content_character(self):
        """Test building complete QC content for character."""
        from core.qc_builder import QCData, build_qc_content
        
        qc_data = QCData(
            model_type="CHARACTER",
            model_name="test_char",
            material_paths=["models/player"],
            sequences=[{"name": "idle", "file": "idle", "fps": 30}],
            include_default_anims="m_anm.mdl"
        )
        
        content = build_qc_content(qc_data)
        
        assert '$modelname "test_char.mdl"' in content
        assert '$sequence "idle"' in content
        assert '$includemodel "m_anm.mdl"' in content


class TestQCFileWriting:
    """Tests for writing QC files to disk."""
    
    def test_write_qc_file_from_data(self):
        """Test writing QC file to disk."""
        from core.qc_builder import QCData, write_qc_file_from_data
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test_model.qc")
            
            qc_data = QCData(
                model_type="PROP",
                model_name="test_model",
                output_path=output_path,
                material_paths=["models/test"]
            )
            
            result_path = write_qc_file_from_data(qc_data)
            
            assert os.path.exists(result_path)
            
            with open(result_path, 'r') as f:
                content = f.read()
            
            assert '$modelname "test_model.mdl"' in content
    
    def test_write_qc_file_adds_extension(self):
        """Test that .qc extension is added if missing."""
        from core.qc_builder import QCData, write_qc_file_from_data
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test_model")  # No extension
            
            qc_data = QCData(
                model_type="PROP",
                model_name="test",
                output_path=output_path
            )
            
            result_path = write_qc_file_from_data(qc_data)
            
            assert result_path.endswith(".qc")
    
    def test_write_qc_file_no_output_path(self):
        """Test that ValueError is raised when no output path."""
        from core.qc_builder import QCData, write_qc_file_from_data
        
        qc_data = QCData(model_name="test", output_path="")
        
        with pytest.raises(ValueError):
            write_qc_file_from_data(qc_data)


class TestLegacyAPI:
    """Tests for backwards-compatible legacy API."""
    
    def test_populate_template(self):
        """Test populate_template function."""
        from core.qc_builder import populate_template
        
        result = populate_template("modelname.txt", {"mdlModelName": "test"})
        
        assert '$modelname "test.mdl"' in result
    
    def test_load_qc_section_order(self):
        """Test load_qc_section_order function."""
        from core.qc_builder import load_qc_section_order
        
        result = load_qc_section_order()
        
        assert "PROP" in result
        assert "CHARACTER" in result
        assert "NPC" in result
