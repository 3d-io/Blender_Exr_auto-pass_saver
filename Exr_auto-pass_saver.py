bl_info = {
    "name": "Exr Auto Pass Saver",
    "description": "Link all render passes to an EXR Multi-Pass File Output",
    "blender": (2, 80, 0),
    "category": "Compositing",
    "author": "3d-io",
    "version": (1, 1),
    "location": "Compositor Tab > Sidebar > Exr Auto Pass Saver",
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


class Exr_Auto_Pass_Linker(bpy.types.Operator):
    bl_idname = "node.exr_pass_linker"
    bl_label = "Exr Auto Linker"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description="Create and link an EXR file output next to the currently selected Render Layers node"

    def RelinkLayers(self, context):
        selected = context.selected_nodes

        for node in selected:
            if node.bl_idname == "CompositorNodeRLayers":
                x = node.location.x + 600
                y = node.location.y 
                outputNode = Exr_Auto_Pass_Saver.CreateNodeFileOutput(self, (x, y))
                Exr_Auto_Pass_Saver.LinkRenderLayers(self, node, outputNode)

    # Exr Auto Saver button
    # Generates reqired nodes for the OpenEXR output and links available render passes
    def execute(self, context):
        self.RelinkLayers(context)
        return {'FINISHED'}

class Exr_Auto_Pass_Saver(bpy.types.Operator):
    bl_idname = "node.exr_pass_saver"
    bl_label = "Exr Auto Saver"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description="Create an EXR file output and Render Layers at the default postion"


    # removes all currently existing nodes
    def cleannodes(self):
        nodesField = bpy.context.scene.node_tree
        for currentNode in nodesField.nodes:
            nodesField.nodes.remove(currentNode)

    # opens the directory of the current render path
    def openfolder(self):
        path = bpy.data.scenes["Scene"].render.filepath
        subprocess.call("explorer " + path, shell=True)

    # returns a target render path taken from the scene's render output and cleaned up as needed
    def GetOutputPathStr(self, layer=""):
        defaultPath = bpy.context.scene.render.filepath
        dirname = os.path.dirname(defaultPath)

        if not dirname.endswith( ('/', '\\') ):
            dirname += "/"
        if not dirname:
            dirname = os.path.expanduser('~') + "/"
        fileName = "output"
        fullPath = dirname + fileName
        return fullPath

    # creates a new Render Layers node at the given position
    def CreateNodeRenderLayers(self, position):
        node = bpy.context.scene.node_tree.nodes.new('CompositorNodeRLayers')
        node.location = position
        return node

    # creates a new Output File node at the given position
    def CreateNodeFileOutput(self, position):
        filepath = bpy.data.filepath
        directory = os.path.dirname(filepath)

        bpy.context.scene.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
        node = bpy.context.scene.node_tree.nodes.new("CompositorNodeOutputFile")
        node.label = 'EXR-MultiLayer'
        node.base_path = directory
        node.location = position
        node.width = 300
        node.use_custom_color = True
        node.color = (0.686, 0.204, 0.176)
        return node

    # links all outputs of the source node to inputs of the target node
    def LinkRenderLayers(self, sourceNode, targetNode):
        for out in sourceNode.outputs:
            # skip disabled outputs
            if (out.enabled == False):
                continue
            slot = 0
            found = False
            for src in targetNode.inputs:
                if (src.identifier == out.identifier):
                    # target node already has matching input, link to it
                    found = True
                    bpy.context.scene.node_tree.links.new(out, targetNode.inputs[slot])
                    break
                slot = slot + 1
            if not found:
                # target node has no matching input, create one and link to it
                targetNode.file_slots.new(out.identifier)
                bpy.context.scene.node_tree.links.new(out, targetNode.inputs[-1])

    # Exr Auto Saver button
    # Generates reqired nodes for the OpenEXR output and links available render passes
    def execute(self, context):
        scene = bpy.context.scene # get the scene

        if not scene.use_nodes:
            print('Info: node_tree not in use. Skipping')
            return {'CANCELLED'}

        if scene.exr_auto_pass_saver_clear_all:
            self.cleannodes()

        if scene.exr_auto_pass_saver_open_dir:
            self.openfolder()

        layersNode = self.CreateNodeRenderLayers((0, 400))
        outputNode = self.CreateNodeFileOutput((400, 450))
        self.LinkRenderLayers(layersNode, outputNode)
        return {'FINISHED'}

class Exr_Auto_Pass_Saver_Panel(bpy.types.Panel):
    bl_label = "Exr Auto Pass Saver"
    bl_category = "Exr Auto Pass Saver"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Link all nodes:")
        sce = context.scene

        # draw Auto Saver button
        row = layout.row()
        row.scale_y = 2.0
        row.operator(Exr_Auto_Pass_Saver.bl_idname, icon='TRACKING_FORWARDS')
        # draw the checkbox (implied from property type = bool)
        layout.prop(sce, "exr_auto_pass_saver_clear_all") 
        layout.prop(sce, "exr_auto_pass_saver_open_dir") 

        # draw Auto Linker button
        row = layout.row()
        row.scale_y = 2.0
        row.operator(Exr_Auto_Pass_Linker.bl_idname, icon="LINKED")
        
        

 

classes = (
    Exr_Auto_Pass_Saver_Panel, 
    Exr_Auto_Pass_Saver, 
    Exr_Auto_Pass_Linker)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
