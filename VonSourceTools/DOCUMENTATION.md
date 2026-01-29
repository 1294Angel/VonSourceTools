# VonSourceTools Developer Documentation

## Overview

VonSourceTools is a comprehensive Blender addon for creating Source Engine content. It provides tools for QC file generation, material/texture conversion, SMD export, and animation workflows.

**Version:** 1.0.0  
**Blender Compatibility:** 4.0+  
**Author:** VonSource Team

---

## Table of Contents

1. [Installation](#installation)
2. [Architecture](#architecture)
3. [Module Reference](#module-reference)
4. [Configuration](#configuration)
5. [External Tools](#external-tools)
6. [API Reference](#api-reference)
7. [Extending the Addon](#extending-the-addon)
8. [Testing](#testing)

---

## Installation

### Standard Installation

1. Download `VonSourceTools.zip`
2. In Blender: Edit → Preferences → Add-ons → Install
3. Select the zip file and enable the addon

### Developer Installation

```bash
# Clone or extract to Blender's addon directory
# Windows: %APPDATA%\Blender Foundation\Blender\<version>\scripts\addons\
# Linux: ~/.config/blender/<version>/scripts/addons/
# macOS: ~/Library/Application Support/Blender/<version>/scripts/addons/

cd <addons_directory>
unzip VonSourceTools.zip
```

### External Tool Setup

For VTF conversion, you need VTFCmd.exe:

1. **Bundled Method (Recommended):** Place `VTFCmd.exe` in `refactor/tools/vtfcmd/`
2. **Manual Method:** Specify the path in the UI

---

## Architecture

### Directory Structure

```
refactor/
├── __init__.py              # Main addon entry point
├── core/                    # Business logic (no Blender registration)
│   ├── __init__.py
│   ├── collision.py         # Collision mesh generation
│   ├── delta_anim.py        # Delta animation processing
│   ├── material_vtf.py      # Material to VTF conversion
│   ├── qc_builder.py        # QC file generation
│   ├── sequences.py         # Animation sequence handling
│   ├── smd_export.py        # SMD export functionality
│   ├── studiomdl.py         # StudioMDL integration
│   └── vtf_conversion.py    # Image format conversion
├── data/                    # Static data and configuration
│   ├── __init__.py
│   ├── constants.py         # Global constants and enums
│   ├── paths.py             # Path configuration (TOOL PATHS HERE)
│   └── valvebiped_bones.py  # Valve biped bone definitions
├── operators/               # Blender operators
│   ├── __init__.py
│   ├── delta_anim_operators.py
│   ├── material_vtf_operators.py
│   ├── qc_operators.py
│   ├── smd_operators.py
│   ├── studiomdl_operators.py
│   └── vtf_operators.py
├── properties/              # Blender property groups
│   ├── __init__.py
│   ├── material_vtf_properties.py
│   ├── qc_properties.py
│   ├── sequence_properties.py
│   └── toolbox_properties.py
├── ui/                      # UI panels (one file per section)
│   ├── __init__.py
│   ├── parent_panel.py
│   ├── qc_panels.py
│   ├── delta_anim_panels.py
│   ├── vmt_generator_panels.py
│   ├── image_converter_panel.py
│   └── smd_export_panel.py
├── utils/                   # Utility functions
│   ├── __init__.py
│   ├── blender_utils.py     # Blender-specific utilities
│   └── file_utils.py        # File system utilities
├── storeditems/             # Bundled data files
│   ├── deltaanimtrick/      # Delta animation reference files
│   └── qcgenerator/         # QC templates
└── tools/                   # External tools
    └── vtfcmd/              # Place VTFCmd.exe here
        └── README.txt
```

### Design Principles

1. **Separation of Concerns:** Core logic is separate from Blender registration
2. **Modular UI:** Each panel section in its own file
3. **Relative Imports:** All internal imports use relative paths (`from ..core import`)
4. **Testability:** Core modules can be unit tested without Blender

---

## Module Reference

### Core Modules

#### `core/material_vtf.py`

Handles conversion of Blender materials to VTF/VMT format.

**Key Functions:**

```python
def get_image_texture_node(material) -> Optional[Node]:
    """Extract the image texture node from a material's Principled BSDF."""

def validate_image_texture(image_node) -> Tuple[Optional[str], Optional[str]]:
    """Validate image and return (path, error_message)."""

def generate_vmt_content(material_name, vmt_params, shader_type, ...) -> str:
    """Generate VMT file content with all shader parameters."""

def build_vtfcmd_command(...) -> List[str]:
    """Build command line arguments for VTFCmd.exe."""

def execute_vtfcmd(command_line) -> Tuple[bool, str, str]:
    """Execute VTFCmd and return (success, stdout, stderr)."""
```

#### `core/qc_builder.py`

Generates QC files for Source Engine models.

#### `core/delta_anim.py`

Processes delta animations for character customization.

### Data Modules

#### `data/paths.py`

**IMPORTANT: External tool paths are configured here.**

```python
# At the top of data/paths.py:

# VTFCmd.exe location
VTFCMD_PATH = None  # Set to override bundled version

# StudioMDL location  
STUDIOMDL_PATH = None  # Set to your Source SDK path
```

**Path Resolution Functions:**

```python
def get_vtfcmd_path() -> Optional[Path]:
    """
    Resolution order:
    1. VTFCMD_PATH constant (if set)
    2. Bundled: addon/tools/vtfcmd/VTFCmd.exe
    3. None (uses UI path)
    """

def get_addon_directory() -> Path:
    """Returns the addon's root directory."""

def get_tools_directory() -> Path:
    """Returns addon/tools/ directory."""
```

### Properties

#### `properties/material_vtf_properties.py`

```python
class VMT_Parameters(PropertyGroup):
    """Per-material VMT shader parameters."""
    enable_phong: BoolProperty
    phong_boost: FloatProperty
    enable_rimlight: BoolProperty
    # ... etc

class VMT_MaterialListItem(PropertyGroup):
    """Material list item with checkbox and VMT params."""
    material_checkbox: BoolProperty
    material_name: StringProperty
    material: PointerProperty(type=bpy.types.Material)
    vmt_params: PointerProperty(type=VMT_Parameters)
```

### Operators

All operators follow the naming convention: `VON<MODULE>_OT_<action>`

| Operator ID | Description |
|-------------|-------------|
| `von.vtf_refresh_materials` | Refresh material list from scene |
| `von.vtf_convert_materials` | Convert materials to VTF |
| `von.vtf_select_all` | Select all materials |
| `von.vtf_deselect_all` | Deselect all materials |
| `von.qcgenerator_prop` | Generate QC for props |
| `von.qcgenerator_character` | Generate QC for characters |
| `von.batchconvertfiletypes` | Batch convert image formats |

---

## Configuration

### Tool Paths

Edit `refactor/data/paths.py` to configure external tool locations:

```python
# Option 1: Use bundled VTFCmd (place in tools/vtfcmd/)
VTFCMD_PATH = None

# Option 2: Specify absolute path
VTFCMD_PATH = Path("C:/Program Files/VTFEdit/VTFCmd.exe")

# StudioMDL configuration
STUDIOMDL_PATH = Path("C:/Steam/steamapps/common/Team Fortress 2/bin/studiomdl.exe")
```

### Scene Properties

The addon registers these scene properties:

| Property | Type | Description |
|----------|------|-------------|
| `von_mats_collection` | CollectionProperty | Material list for VTF conversion |
| `von_mats_index` | IntProperty | Selected material index |
| `von_vtfcmd_path` | PointerProperty | VTFCmd directory path |
| `von_material_output_path` | PointerProperty | Output directory |
| `von_vtf_format` | EnumProperty | VTF compression format |
| `von_vmt_generate_bool` | BoolProperty | Enable VMT generation |

---

## External Tools

### VTFCmd

**Source:** [Nem's Tools](https://nemstools.github.io/pages/VTFLib.html)

**Installation:**
1. Download VTFCmd from Nem's Tools
2. Extract to `refactor/tools/vtfcmd/`
3. Required files: `VTFCmd.exe`, `VTFLib.dll`

**Supported Formats:**
- Input: PNG, TGA, JPG, BMP, DDS
- Output: VTF (Valve Texture Format)

### StudioMDL

Part of Source SDK. Used for compiling QC files to MDL.

---

## API Reference

### Registering New Panels

```python
# In ui/my_new_panel.py
import bpy

class VON_PT_my_panel(bpy.types.Panel):
    bl_idname = "VON_PT_my_panel"
    bl_label = "My Panel"
    bl_parent_id = "VON_PT_parent"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonSourceTools'
    
    def draw(self, context):
        layout = self.layout
        # ... draw UI

CLASSES = [VON_PT_my_panel]

def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
```

Then add to `ui/__init__.py`:

```python
from . import my_new_panel

MODULES = [
    parent_panel,
    # ... other modules
    my_new_panel,
]
```

### Adding New Operators

```python
# In operators/my_operators.py
import bpy
from bpy.types import Operator

class VON_OT_my_operator(Operator):
    bl_idname = "von.my_operator"
    bl_label = "My Operator"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        # ... do work
        return {'FINISHED'}

CLASSES = [VON_OT_my_operator]

def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
```

---

## Extending the Addon

### Adding VMT Shader Parameters

1. Add property to `VMT_Parameters` in `properties/material_vtf_properties.py`
2. Add UI element in `ui/vmt_generator_panels.py`
3. Update `generate_vmt_content()` in `core/material_vtf.py`

### Adding New QC Commands

1. Create template in `storeditems/qcgenerator/templates/commands/`
2. Update `core/qc_builder.py` to use the template
3. Add UI controls in `ui/qc_panels.py`

---

## Testing

### Running Tests

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all unit tests (no Blender required)
pytest tests/ -v -m "not integration and not smoke"

# Run integration tests (requires Blender)
export BLENDER_PATH="/path/to/blender"
pytest tests/ -v -m integration

# Run with coverage
pytest tests/ -v --cov=refactor --cov-report=html
```

### Test Structure

```
tests/
├── conftest.py                    # Fixtures and Blender runner
├── test_core.py                   # Core module tests
├── test_material_vtf_core.py      # Material VTF logic tests
├── test_material_vtf_operators.py # Operator structure tests
├── test_material_vtf_properties.py# Property tests
├── test_material_vtf_integration.py # Blender integration tests
├── test_operators.py              # General operator tests
├── test_properties.py             # General property tests
├── test_ui.py                     # UI structure tests
└── test_smoke.py                  # End-to-end workflow tests
```

### Writing Tests

```python
# Unit test (no Blender)
def test_my_function(mock_bpy):
    from core.my_module import my_function
    result = my_function()
    assert result == expected

# Integration test (requires Blender)
@pytest.mark.integration
@requires_blender
def test_operator_in_blender():
    result = run_addon_test_in_blender('''
        bpy.ops.von.my_operator()
        test_output.append("success")
    ''')
    assert result['success']
```

---

## Troubleshooting

### Common Issues

**"No module named 'core'"**
- Ensure all imports use relative paths: `from ..core import`

**VTFCmd not found**
- Place VTFCmd.exe in `refactor/tools/vtfcmd/`
- Or set `VTFCMD_PATH` in `data/paths.py`
- Or specify path in the UI

**Material has no Image Texture node**
- Ensure material uses Principled BSDF
- Connect an Image Texture to Base Color input

---

## License

[Specify your license here]

## Credits

See `credits.txt` for full attribution.
