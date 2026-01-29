# VonSourceTools v1.0.0
I've had the documentation AI generated because it's driving me insane xD You'll have to forgive that
#
The ultimate Blender addon for Source Engine content creation. Streamline your workflow with integrated tools for materials, models, and animations.

## ✨ Features

### 🎨 Material to VTF Converter
- Automatically extract textures from Blender materials and convert to VTF format
- Generate VMT files with proper shader parameters
- Support for multiple texture types (diffuse, normal, specular, etc.)
- Batch processing of multiple materials at once
- Configurable VTF compression and format options

### 📄 QC Generator
- Template-based QC file generation for Source Engine models
- Support for multiple model types:
  - **Props** - Static and physics props
  - **Characters** - Player models with full animation support
  - **NPCs** - Non-player characters
  - **Viewmodels** - First-person weapon/item models
  - **Worldmodels** - Third-person weapon/item models
- Bodygroup management with collection-based workflow
- Animation sequence collection from armatures
- Activity assignment with categorized dropdown menus
- Surface property selection with organized categories
- Collision model configuration

### 🦴 Delta Animation Trick
- One-click delta animation setup for Source Engine characters
- Automatic ValveBiped bone validation with configurable similarity threshold
- Reference armature importing (male/female/proportions)
- Step-by-step advanced mode for manual control

### 🖼️ Image Filetype Converter
- Batch convert between image formats (PNG, JPG, TGA, BMP, PSD, HDR, EXR, VTF)
- Preserves folder structure during conversion
- Background processing to keep Blender responsive

### 📦 Batch SMD Export
- Split objects into temporary collections for organized export
- Restore original collection structure after export
- Streamlined workflow for multi-mesh model

## ⚙️ Requirements

- **Blender 2.80+** (tested on 3.x and 4.x)
- **VTFCmd.exe** - Required for VTF conversion features
- **Blender Source Tools** - Required for SMD export functionality

## 📥 Installation

1. Download `VonSourceTools.zip`
2. In Blender: Edit → Preferences → Add-ons → Install
3. Select the downloaded zip file
4. Enable "VonSourceTools" in the addon list

## 🎯 Quick Start

1. Open the VonSourceTools panel in the 3D View sidebar (N panel)
2. Expand the desired tool section
3. Configure settings and click the main action button


## 🙏 Credits

- Delta Animation Trick methodology from the Source modding community (Special mention to sksh70: https://github.com/sksh70/proportion_trick_script)
- VTFCmd by Nem's Tools
- Blender Source Tools for making exporting smd's possible
- Material_To_VTF addon by Graves (grvs), privately sent over discord. Absolutely amazing stuff!

---


