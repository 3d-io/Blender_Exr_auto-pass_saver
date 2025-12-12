# Blender EXR Auto Pass Saver

Automatically link all render passes in Blender to a single **Multi-Layer OpenEXR output**.

**EXR Auto Pass Saver** is a Blender Python add-on that creates a **Multi-Layer OpenEXR output node**, collects all available render passes, and connects them automatically — saving time and avoiding manual node setup.

![Blender UI Preview](https://github.com/3d-io/Blender_Exr_auto-pass_saver/blob/master/Exr_Auto_Pass_Saver_UI_Blender.png)

---

## What it does

- Automatically creates a **Multi-Layer OpenEXR output node**
- Collects and links **all enabled render passes**
- Works with **any Blender renderer** that supports Multi-Layer passes
- Ideal for **compositing, retouching, and post-production**

Multi-Layer EXR images generated in Blender are optimal for workflows in tools such as:
- Adobe Photoshop  
- Fusion  
- Nuke  

![Photoshop preview of created Multilayer EXR Image](https://github.com/3d-io/Blender_Exr_auto-pass_saver/blob/master/Exr_Auto_Pass_Saver_Imported_in_Photoshop.png)

---

## Photoshop Support (Free EXR-IO Plugin)

To open and edit **Multi-Layer OpenEXR files in Adobe Photoshop**, we recommend the **free EXR-IO plugin**.

EXR-IO allows Photoshop to read and write:
- Multi-Layer OpenEXR files
- Render passes
- High-dynamic-range (HDR) image data

👉 **Download the free EXR-IO plugin here:**  
https://www.exr-io.com

![EXR workflow preview](https://github.com/3d-io/Blender_Exr_auto-pass_saver/blob/master/images/exr_auto-pass_saver.gif)

---

## 🚀 Installation (Recommended)

### Install via ZIP (Drag & Drop)

1. Click **Code → Download ZIP** on this GitHub page  
2. Open **Blender**
3. Drag & drop the downloaded **ZIP file directly into the Blender window**
4. Blender will automatically install the add-on
5. Go to **Edit → Preferences → Add-ons**
6. Search for **EXR Auto Pass Saver**
7. Enable the add-on ☑

✅ No manual copying required.

---

### Alternative: Manual Installation

1. Download the ZIP file
2. Extract it
3. Copy the folder into: Blender/<version>/scripts/addons/
4. Restart Blender
5. Enable the add-on in **Preferences → Add-ons**

---

## Compatibility

- Blender versions supporting **Multi-Layer OpenEXR**
- Cycles / Eevee (pass support dependent on renderer)


