# Blender EXR Auto Pass Saver
Link all render passes in Blender to a new EXR-mulitlayer save node
![Blender UI Preview](images/Exr_Auto_Pass_Saver_UI_Blender.png)
<br/><br/>

EXR Auto Saver will automatically create a Render Layer Node and EXR File Output node linked together at the default position on the compositor.
![Blender UI EXR Auto Saver Demo](images/exr_auto-pass_saver.gif)<br/>

(v1.1) EXR Auto Linker will automatically link an EXR File Output node to an <b>EXISTING</b> Render Layer node, offset to the right of the existing node.
![Blender UI EXR Auto Linker Demo](images/EXR_LINKER_DEMO.gif)<br/>

MultiLayer EXR images created in Blender are optimal image editing material for compositing or retouching in applications like Adobe Photoshop, Fusion or Nuke.
![Photoshop preview of created Multilayer Exr Image](images/Exr_Auto_Pass_Saver_Imported_in_Photoshop.png)<br/>

This script works in combination with any Blender renderer supporting Mulitlayer Pass Nodes.<br/>
They can be imported in Photoshop using Exr-IO importer.<br/>
You can get the free Exr-IO Importer from <b>www.exr-io.com</b><br/>



# Installation
1. Unzip the folder
2. Edit -> Preferences -> Install Addon:
3. Find the .py file and double click on it
4. In the Addons menu enable the plugin
