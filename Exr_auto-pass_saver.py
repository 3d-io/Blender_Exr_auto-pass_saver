bl_info = {
    "name": "Exr Auto Pass Saver",
    "description": "Link all render passes to a new EXR-mulitlayer save node",
    "blender": (2, 80, 0),
    "category": "Compositing",
    "author": "3d-io",
    "version": (1, 0),
    "location": "Compositor Tab > Sidebar > Exr Auto Save Pass Saver",
    "warning": "BSD",
    "wiki_url": "https://github.com/3d-io/",
    "support": "COMMUNITY",
}

import bpy
import subprocess
import os

bpy.types.Scene.exr_auto_pass_saver_clear_all = bpy.props.BoolProperty(
    name="Clear all nodes",
        description="Remove all nodes from the Compositor and add only RenderLayer <-> Saver Node",
        default = False)



bpy.types.Scene.exr_auto_pass_saver_open_dir = bpy.props.BoolProperty(
    name="Open destination folder",
        description="A folder where the Exr Image is going to be saved",
        default = False)


class Exr_Auto_Pass_Saver(bpy.types.Operator):
    bl_idname = "node.exr_pass_saver"
    bl_label = "Exr Auto Saver"
    bl_options = {'REGISTER', 'UNDO'}

    def cleannodes(self):
        nodesField = bpy.context.scene.node_tree
        for currentNode in nodesField.nodes:
            nodesField.nodes.remove(currentNode)
    
    def openfolder(self):
        mypath = bpy.data.scenes["Scene"].render.filepath
        subprocess.call("explorer " + mypath, shell=True)

    def GetOutputPathStr(self):
        defaultPath = bpy.context.scene.render.filepath
        dirname = os.path.dirname(defaultPath)
        if not dirname.endswith( ('/', '\\') ):
            dirname += "/"
        if not dirname:
            dirname = os.path.expanduser('~') + "/"
        fileName = "output"
        fullPath = dirname + fileName
        return fullPath

    def execute(self, context):
        scene = bpy.context.scene # get the scene

        #If UseNode Checker Box is Off do Nothing!
        if scene.use_nodes is False:
            print('Info: node_tree not in use. Skipping')
            return {'CANCELLED'}
            
        # If CheckerBox is On, clear all Compositor!
        if scene.exr_auto_pass_saver_clear_all == True:
            self.cleannodes()
            
        # If CheckerBox is On, Open Folder!
        if scene.exr_auto_pass_saver_open_dir == True:
            self.openfolder()
        
        scene.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
        
        image_node = scene.node_tree.nodes.new('CompositorNodeRLayers')
        RLayerPosition = 0,400
        image_node.location = RLayerPosition


        output_file = scene.node_tree.nodes.new("CompositorNodeOutputFile") # create save node
        output_file.label = 'EXR-MultiLayer'

        output_file.base_path = self.GetOutputPathStr()



        output_file.location = RLayerPosition[0] + 400, RLayerPosition[1] + 50
        output_file.width = 300
        output_file.width_hidden = 300
 
        for out in image_node.outputs:     
            if (out.enabled == False):
                continue

            slot = 0
            found = False

            for src in output_file.inputs:
                if (src.identifier == out.identifier):
                    found = True
                    break
                slot = slot + 1

            if found == False:
                output_file.file_slots.new(out.identifier)
                scene.node_tree.links.new(out, output_file.inputs[-1])
            else:
                scene.node_tree.links.new(out, output_file.inputs[slot])


        output_file.use_custom_color = True
        output_file.color = (0.686, 0.204, 0.176)
        return {'FINISHED'}



class Exr_Auto_Pass_Saver_Panel(bpy.types.Panel):
    bl_label = "Exr Auto Pass Saver"
    bl_category = "Exr Auto Pass Saver"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Link all nodes:")
        row = layout.row()
        row.scale_y = 2.0
        row.operator(Exr_Auto_Pass_Saver.bl_idname, icon='TRACKING_FORWARDS')
        
        #layout.operator(Exr_Auto_Pass_Saver.bl_idname, icon='TRACKING_FORWARDS')
        
        sce = context.scene
        # draw the checkbox (implied from property type = bool)
        layout.prop(sce, "exr_auto_pass_saver_clear_all") 
        layout.prop(sce, "exr_auto_pass_saver_open_dir") 

classes = (Exr_Auto_Pass_Saver_Panel, Exr_Auto_Pass_Saver)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
