# VonSourceTools Test Suite

This test suite provides comprehensive testing for the VonSourceTools Blender addon, including unit tests, integration tests, and smoke tests.

## Test Categories

### Unit Tests (No Blender Required)
- Fast tests that mock the Blender API
- Test pure Python logic in isolation
- Run without Blender installed

### Integration Tests (Blender Required)
- Test addon registration and property groups
- Verify operators are registered correctly
- Test Blender API interactions

### Smoke Tests (Blender Required)
- Full workflow tests
- End-to-end functionality verification
- Test real-world usage scenarios

## Setup

### 1. Install Test Dependencies

```bash
pip install -r requirements-test.txt
```

### 2. Configure Blender Path (for integration/smoke tests)

Set the `BLENDER_PATH` environment variable:

```bash
# Linux/macOS
export BLENDER_PATH="/path/to/blender"

# Windows (PowerShell)
$env:BLENDER_PATH = "C:\Path\To\blender.exe"

# Windows (CMD)
set BLENDER_PATH=C:\Path\To\blender.exe
```

Or create a `.env` file in the project root:
```
BLENDER_PATH=/path/to/blender
```

## Running Tests

### From VSCode

1. Install the Python extension
2. Open the Command Palette (Ctrl+Shift+P)
3. Select "Python: Configure Tests"
4. Choose "pytest"
5. Select "tests" as the test directory
6. Use the Test Explorer in the sidebar

### From Command Line

```bash
# Run all tests
pytest tests/ -v

# Run only unit tests (fast, no Blender needed)
pytest tests/ -v -m "not integration and not smoke"

# Run integration tests
pytest tests/ -v -m integration

# Run smoke tests
pytest tests/ -v -m smoke

# Run with coverage report
pytest tests/ -v --cov=refactor --cov-report=html

# Run specific test file
pytest tests/test_data.py -v

# Run specific test class
pytest tests/test_data.py::TestConstants -v

# Run specific test
pytest tests/test_data.py::TestConstants::test_model_type_category_map_exists -v

# Run tests in parallel (requires pytest-xdist)
pytest tests/ -v -n auto
```

## Test Structure

```
tests/
├── conftest.py           # Pytest configuration and fixtures
├── test_data.py          # Tests for data module
├── test_utils.py         # Tests for utils module
├── test_core.py          # Tests for core module
├── test_integration.py   # Integration tests (require Blender)
└── test_smoke.py         # Smoke tests (full workflows)
```

## Writing New Tests

### Unit Test Example

```python
import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "refactor"))

class TestMyFeature:
    def test_something(self):
        from my_module import my_function
        result = my_function()
        assert result == expected_value
```

### Integration Test Example

```python
import pytest
from conftest import run_addon_test_in_blender, requires_blender, integration

@pytest.mark.integration
@requires_blender
class TestMyBlenderFeature:
    def test_something_in_blender(self):
        result = run_addon_test_in_blender('''
    # Python code that runs inside Blender
    scene = bpy.context.scene
    test_output.append("Test passed")
''')
        assert result['success'], result['error']
```

### Using Mocks

```python
def test_with_mock_bpy(self, mock_bpy):
    """Test that uses the mock_bpy fixture."""
    from utils.blender_utils import object_exists
    
    # Setup mock
    mock_bpy.data.objects['TestObject'] = True
    
    # Test
    result = object_exists("TestObject")
    assert result is True
```

## Fixtures

### `mock_bpy`
Provides a mock Blender `bpy` module for unit testing.

### `mock_bpy_with_armature`
Extends `mock_bpy` with a sample armature object.

## Test Markers

- `@pytest.mark.integration` - Marks tests that require Blender
- `@pytest.mark.smoke` - Marks end-to-end workflow tests
- `@pytest.mark.slow` - Marks slow-running tests
- `@requires_blender` - Skips test if Blender is not available

## Troubleshooting

### Tests Can't Find Blender

1. Verify Blender is installed
2. Check the `BLENDER_PATH` environment variable
3. Ensure the path points to the Blender executable (not the .app bundle on macOS)

### Import Errors

1. Make sure you're running from the project root
2. Check that `sys.path` includes the refactor directory
3. Verify the addon structure is correct

### Mock-Related Failures

1. Check that you're using `with patch.dict(sys.modules, {'bpy': mock_bpy})`
2. Ensure the mock fixture is being passed to the test function
3. Verify mock setup matches expected Blender API structure

## Coverage Reports

Generate an HTML coverage report:

```bash
pytest tests/ --cov=refactor --cov-report=html
```

Open `htmlcov/index.html` in a browser to view the report.

## Continuous Integration

Example GitHub Actions workflow:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements-test.txt
      - run: pytest tests/ -v -m "not integration and not smoke"

  integration-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install Blender
        run: |
          sudo snap install blender --classic
      - run: pip install -r requirements-test.txt
      - run: pytest tests/ -v -m integration
        env:
          BLENDER_PATH: /snap/bin/blender
```
