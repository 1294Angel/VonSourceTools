# VonSourceTools User Manual

## Welcome to VonSourceTools!

VonSourceTools is your all-in-one Blender addon for creating Source Engine content. Whether you're making props, characters, or animations for games like Team Fortress 2, Counter-Strike, Garry's Mod, or any Source Engine game, this addon streamlines your workflow.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Material to VTF Converter](#material-to-vtf-converter)
3. [QC Generator](#qc-generator)
4. [Delta Animation Tools](#delta-animation-tools)
5. [Image Converter](#image-converter)
6. [SMD Export](#smd-export)
7. [Troubleshooting](#troubleshooting)
8. [Glossary](#glossary)

---

## Getting Started

### Installation

1. Download `VonSourceTools.zip`
2. Open Blender
3. Go to **Edit → Preferences → Add-ons**
4. Click **Install** and select the zip file
5. Enable "VonSourceTools" in the addon list

### Finding the Tools

All VonSourceTools panels are located in:
- **3D Viewport → Sidebar (N key) → VonSourceTools tab**

### Setting Up VTFCmd (Required for VTF Conversion)

To convert textures to VTF format, you need VTFCmd:

1. Download VTFCmd from [Nem's Tools](https://nemstools.github.io/pages/VTFLib.html)
2. Extract the files
3. **Easy Setup:** Copy `VTFCmd.exe` and `VTFLib.dll` to:
   ```
   [Blender Addons]/VonSourceTools/refactor/tools/vtfcmd/
   ```
4. **Alternative:** Specify the VTFCmd folder path in the UI

---

## Material to VTF Converter

Convert your Blender materials directly to Source Engine VTF textures and VMT material files.

### What It Does

- Extracts textures from Blender materials
- Converts images to VTF format (Source Engine texture format)
- Generates VMT files with advanced shader settings (phong, rim lighting, etc.)
- Supports normal maps and specular/phong exponent maps

### Quick Start

1. **Set up your materials** in Blender using Principled BSDF with Image Textures
2. **Open the Material to VTF Converter** panel
3. **Click "Refresh"** to populate the material list
4. **Set your output path** (should be inside a `materials` folder)
5. **Click "Convert to VTF"**

### Step-by-Step Guide

#### 1. Prepare Your Materials

Your Blender materials should be set up like this:

```
Principled BSDF
└── Base Color ← Image Texture (your diffuse/albedo texture)
```

The addon reads the image connected to the Base Color input.

#### 2. Select Materials

- Click **Refresh** to scan all objects in your scene
- Use checkboxes to select which materials to convert
- **All** selects all materials
- **None** deselects all materials

#### 3. Configure Paths

- **VTFCmd Path:** Shows "Found (bundled)" if VTFCmd is in the tools folder
- **Material Output Path:** Where to save VTF/VMT files
  - Should be inside your game's `materials` folder
  - Example: `C:/Steam/steamapps/common/GarrysMod/garrysmod/materials/models/mymodel/`

#### 4. VTF Settings

| Setting | Description |
|---------|-------------|
| **Format** | DXT1 (no alpha), DXT3/DXT5 (with alpha) |
| **Alpha Format** | Compression for alpha channel |
| **Version** | VTF file version (7.5 recommended) |
| **Enable Resize** | Resize textures to power-of-2 dimensions |
| **Clamp Size** | Maximum texture resolution |

#### 5. VMT Generation (Optional)

Enable **Generate VMT Files** to create material definition files.

**Shader Types:**
- **VertexlitGeneric** - For characters and props (most common)
- **LightmappedGeneric** - For world geometry
- **UnlitGeneric** - No lighting (HUD elements, etc.)

**Global Parameters:**
- **Additive** - Additive blending (glowing effects)
- **Translucent** - Transparency support
- **No Cull** - Render both sides of faces

### VMT Material Settings (Per-Material)

Click on a material in the list to configure its specific VMT settings:

#### Texture Maps
- **Normal Map** - Select a normal/bump map image
- **Phong Exponent Map** - Select a specular/gloss map

#### Phong Shading
Controls specular highlights on your model:
- **Enable Phong** - Turn on specular highlights
- **Phong Boost** - Intensity (1.0 = normal)
- **Phong Albedo Tint** - Tint highlights with base texture color
- **Phong Fresnel Ranges** - Edge vs center reflection balance

#### Rim Lighting
Creates a glowing edge effect:
- **Enable Rim Light** - Turn on rim lighting
- **Rim Light Exponent** - Falloff sharpness (higher = sharper)
- **Rim Light Boost** - Intensity
- **Rim Mask** - Use mask for rim lighting

#### Environment Mapping
Adds reflections:
- **Enable Environment Map** - Turn on reflections
- **Environment Map Tint** - Color/intensity of reflections
- **Normal Alpha Envmap Mask** - Use normal map alpha for reflection mask

---

## QC Generator

Generate QC files for compiling your models with StudioMDL.

### What It Does

- Creates properly formatted QC files
- Supports props and characters
- Configures bodygroups, materials, animations
- Sets collision models and surface properties

### Using the QC Generator

#### 1. Main Settings

- **Model Type:** Choose Prop or Character
- **Output Path:** Where to save the QC file
- **Scale:** Model scale factor

#### 2. Collision Settings

- **Generate Collision:** Auto-create collision mesh
- **Existing Collision Collection:** Use a specific collection for collision

#### 3. Surface Properties

Select the material type for physics:
- Categories: Concrete, Metal, Wood, Flesh, etc.
- Affects footstep sounds, bullet impacts, physics behavior

#### 4. Bodygroups

Define switchable body parts:
1. Click **Refresh Collections**
2. Assign collections to bodygroup slots
3. Each bodygroup can have multiple options (including "blank" for hidden)

#### 5. Materials

Configure material paths for cdmaterials command.

#### 6. Animations (Characters)

Set up animation sequences with activities and events.

---

## Delta Animation Tools

Create delta animations for character customization (body morphs, facial flexes).

### What Are Delta Animations?

Delta animations store the *difference* between a base pose and a modified pose. Source Engine uses these for:
- Body sliders (muscular, skinny, etc.)
- Facial expressions
- Damage states

### Using Delta Animation Tools

1. **Import Reference:** Load the base skeleton
2. **Set Up Proportions:** Configure the proportion targets
3. **Create Deltas:** Generate the delta animation data

### Advanced Settings

- **Bone Selection:** Choose which bones to include
- **Constraint Handling:** Manage bone constraints during export

---

## Image Converter

Batch convert images between formats.

### Supported Conversions

| From | To |
|------|-----|
| PNG, TGA, JPG, BMP | VTF |
| VTF | PNG, TGA |

### Using the Converter

1. Set **Input Folder** - folder with source images
2. Set **Output Folder** - where to save converted images
3. Select **Source Filetype** and **Target Filetype**
4. Click **Run Conversion**

> **Note:** Converting to/from VTF may take a few minutes. Blender may appear frozen but is working.

---

## SMD Export

Export meshes and animations to SMD format for Source Engine.

### Collections Workflow

1. **Split Objects:** Separates objects for proper export hierarchy
2. **Restore Objects:** Undo the split operation

### Export Settings

- **Export Folder:** Destination for SMD files
- Click **Export SMD** to export all configured meshes

---

## Troubleshooting

### VTFCmd Not Found

**Symptom:** Convert button is grayed out or error message

**Solution:**
1. Download VTFCmd from Nem's Tools
2. Place `VTFCmd.exe` in: `[Addon]/refactor/tools/vtfcmd/`
3. Or specify the path manually in the UI

### "Material has no Image Texture node"

**Symptom:** Error when converting materials

**Solution:**
1. Open your material in the Shader Editor
2. Ensure you're using **Principled BSDF**
3. Connect an **Image Texture** node to the **Base Color** input

### Textures Look Wrong In-Game

**Possible Causes:**
- Wrong VTF format (try DXT5 for textures with transparency)
- Missing VMT file
- Incorrect material path in VMT

### VMT Path Issues

The VMT's `$basetexture` path is relative to the `materials` folder.

**Example:**
- Output path: `C:/game/materials/models/mymodel/`
- VMT will reference: `models/mymodel/texturename`

### Blender Freezes During Conversion

This is normal for large texture batches. VTFCmd is processing in the background. Wait for it to complete.

---

## Glossary

| Term | Definition |
|------|------------|
| **VTF** | Valve Texture Format - Source Engine's texture format |
| **VMT** | Valve Material Type - Material definition file |
| **QC** | "Quake C" - Model compilation script |
| **SMD** | Studio Model Data - Mesh/animation format |
| **MDL** | Compiled model file |
| **Phong** | Specular highlight shading |
| **Normal Map** | Texture that adds surface detail without geometry |
| **Delta Animation** | Stores pose differences for morphing |
| **Bodygroup** | Switchable model parts |
| **cdmaterials** | QC command specifying material search paths |
| **$basetexture** | VMT parameter for the main texture |
| **StudioMDL** | Valve's model compiler |

---

## Tips & Best Practices

### Textures
- Use power-of-2 dimensions (256, 512, 1024, 2048)
- DXT1 for opaque textures (smaller file size)
- DXT5 for textures with alpha/transparency
- Keep source files (PSD, PNG) separate from exported VTFs

### Materials
- Name materials clearly (they become VMT filenames)
- Avoid special characters in material names
- Test materials in HLMV (Half-Life Model Viewer) before in-game

### QC Files
- Keep your QC organized with comments
- Use relative paths when possible
- Test compile frequently during development

### Workflow
1. Model in Blender
2. Set up materials with proper textures
3. Convert textures to VTF
4. Export SMD files
5. Generate QC file
6. Compile with StudioMDL
7. Test in HLMV or in-game

---

## Getting Help

- **Bug Reports:** Use the thumbs down button on errors
- **Feature Requests:** Contact the development team
- **Community:** Join Source modding communities for tips

---

## Quick Reference Card

### Keyboard Shortcuts
- **N** - Toggle sidebar (where VonSourceTools panels are)

### File Locations
- **VTFCmd:** `[Addon]/refactor/tools/vtfcmd/VTFCmd.exe`
- **Tool Paths Config:** `[Addon]/refactor/data/paths.py`
- **Templates:** `[Addon]/refactor/storeditems/`

### Common Paths (Windows)
- **Blender Addons:** `%APPDATA%\Blender Foundation\Blender\<version>\scripts\addons\`
- **Source SDK:** `C:\Program Files (x86)\Steam\steamapps\common\<game>\bin\`
- **Game Materials:** `C:\Program Files (x86)\Steam\steamapps\common\<game>\<game>\materials\`

---

*Thank you for using VonSourceTools!*
