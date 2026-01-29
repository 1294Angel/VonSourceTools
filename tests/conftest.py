"""
VonSourceTools Test Suite

This test suite can be run from VSCode using pytest.
It includes:
- Unit tests (no Blender required, uses mocks)
- Integration tests (runs Blender in background)
- Smoke tests (full addon functionality)

Usage:
    # Run all tests
    pytest tests/ -v

    # Run only unit tests (fast, no Blender needed)
    pytest tests/ -v -m "not integration and not smoke"

    # Run integration tests (requires Blender)
    pytest tests/ -v -m integration

    # Run smoke tests (full Blender tests)
    pytest tests/ -v -m smoke

Requirements:
    pip install pytest pytest-mock

Configuration:
    Set BLENDER_PATH environment variable to your Blender executable path
    e.g., export BLENDER_PATH="/path/to/blender"
"""
import os
import sys
import subprocess
import tempfile
import json
from pathlib import Path
from typing import Optional
from unittest.mock import MagicMock, patch

import pytest


# =============================================================================
# Configuration
# =============================================================================

def get_blender_path() -> str:
    """Get the path to the Blender executable."""
    # Check environment variable first
    blender_path = os.environ.get('BLENDER_PATH')
    if blender_path and Path(blender_path).exists():
        return blender_path
    
    # Common paths to check
    common_paths = [
        # Windows
        r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 4.1\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe",
        # macOS
        "/Applications/Blender.app/Contents/MacOS/Blender",
        # Linux
        "/usr/bin/blender",
        "/snap/bin/blender",
    ]
    
    for path in common_paths:
        if Path(path).exists():
            return path
    
    # Try to find in PATH
    try:
        result = subprocess.run(
            ["which", "blender"] if sys.platform != "win32" else ["where", "blender"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip().split('\n')[0]
    except Exception:
        pass
    
    return None


BLENDER_PATH = get_blender_path()
ADDON_PATH = Path(__file__).parent.parent / "refactor"


def blender_available() -> bool:
    """Check if Blender is available for testing."""
    return BLENDER_PATH is not None and Path(BLENDER_PATH).exists()


# =============================================================================
# Blender Mock Setup
# =============================================================================

class MockBlenderModule:
    """Mock bpy module for unit testing without Blender."""
    
    def __init__(self):
        self.data = MagicMock()
        self.context = MagicMock()
        self.types = MagicMock()
        self.props = MagicMock()
        self.ops = MagicMock()
        self.utils = MagicMock()
        
        # Setup common data structures
        self.data.objects = {}
        self.data.collections = {}
        self.data.armatures = {}
        self.data.meshes = {}
        self.data.actions = {}
        
        # Setup context
        self.context.scene = MagicMock()
        self.context.selected_objects = []
        self.context.view_layer = MagicMock()
        self.context.collection = MagicMock()
        self.context.mode = 'OBJECT'
        
        # Setup property types
        self.props.StringProperty = lambda **kwargs: None
        self.props.BoolProperty = lambda **kwargs: None
        self.props.IntProperty = lambda **kwargs: None
        self.props.FloatProperty = lambda **kwargs: None
        self.props.EnumProperty = lambda **kwargs: None
        self.props.CollectionProperty = lambda **kwargs: None
        self.props.PointerProperty = lambda **kwargs: None


@pytest.fixture
def mock_bpy():
    """Fixture that provides a mock bpy module."""
    mock = MockBlenderModule()
    with patch.dict(sys.modules, {'bpy': mock}):
        yield mock


@pytest.fixture
def mock_bpy_with_armature(mock_bpy):
    """Fixture that provides mock bpy with a sample armature."""
    # Create mock armature
    armature = MagicMock()
    armature.name = "TestArmature"
    armature.type = "ARMATURE"
    armature.data = MagicMock()
    armature.data.bones = {
        'ValveBiped.Bip01_Pelvis': MagicMock(name='ValveBiped.Bip01_Pelvis'),
        'ValveBiped.Bip01_Spine': MagicMock(name='ValveBiped.Bip01_Spine'),
        'ValveBiped.Bip01_Head1': MagicMock(name='ValveBiped.Bip01_Head1'),
    }
    armature.pose = MagicMock()
    armature.pose.bones = armature.data.bones
    
    mock_bpy.data.objects['TestArmature'] = armature
    mock_bpy.context.selected_objects = [armature]
    
    return mock_bpy


# =============================================================================
# Blender Test Runner
# =============================================================================

def run_blender_script(script: str, timeout: int = 60) -> tuple:
    """
    Run a Python script inside Blender in background mode.
    
    Args:
        script: Python script to execute
        timeout: Maximum execution time in seconds
    
    Returns:
        tuple: (return_code, stdout, stderr)
    """
    if not blender_available():
        pytest.skip("Blender not available")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(script)
        script_path = f.name
    
    try:
        result = subprocess.run(
            [BLENDER_PATH, '--background', '--python', script_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    finally:
        os.unlink(script_path)


def run_addon_test_in_blender(test_code: str, addon_path: str = None) -> dict:
    """
    Run a test inside Blender with the addon loaded.
    
    Args:
        test_code: Python test code to execute
        addon_path: Path to the addon (defaults to ADDON_PATH)
    
    Returns:
        dict: Test results with 'success', 'output', and 'error' keys
    """
    if addon_path is None:
        addon_path = str(ADDON_PATH)
    
    script = f'''
import sys
import json

# Add addon to path
sys.path.insert(0, r"{addon_path}")

results = {{"success": False, "output": "", "error": ""}}

try:
    import bpy
    
    # Import and register the addon
    from refactor import register, unregister
    register()
    
    # Run the test code
    test_output = []
    
{test_code}
    
    results["success"] = True
    results["output"] = "\\n".join(test_output) if test_output else "Test passed"
    
    # Cleanup
    unregister()
    
except Exception as e:
    import traceback
    results["error"] = traceback.format_exc()

# Output results as JSON
print("TEST_RESULTS_START")
print(json.dumps(results))
print("TEST_RESULTS_END")
'''
    
    returncode, stdout, stderr = run_blender_script(script)
    
    # Extract results from output
    try:
        start = stdout.find("TEST_RESULTS_START") + len("TEST_RESULTS_START")
        end = stdout.find("TEST_RESULTS_END")
        results_json = stdout[start:end].strip()
        return json.loads(results_json)
    except Exception as e:
        return {
            "success": False,
            "output": stdout,
            "error": f"Failed to parse results: {e}\nStderr: {stderr}"
        }


# =============================================================================
# Test Markers
# =============================================================================

# Mark tests that require Blender
integration = pytest.mark.integration
smoke = pytest.mark.smoke

# Skip if Blender not available
requires_blender = pytest.mark.skipif(
    not blender_available(),
    reason="Blender not available"
)
