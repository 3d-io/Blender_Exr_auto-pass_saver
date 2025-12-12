bl_info = {
    "name": "Exr Auto Pass Saver",
    "description": "Link all render passes to a new EXR-MulitLayer save node",
    "blender": (2, 80, 0),
    "category": "Compositing",
    "author": "3d-io",
    "version": (1, 1, 0),
    "location": "Compositor Tab > Sidebar > Exr Auto Pass Saver",
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


    def GetNodeTree(self):
        if bpy.app.version[0] >= 5:
            return bpy.context.scene.compositing_node_group
        else:
            return bpy.context.scene.node_tree


    # removes all currently existing nodes
    def cleannodes(self):
        nodeTree = self.GetNodeTree()
        for currentNode in nodeTree.nodes:
            nodeTree.nodes.remove(currentNode)


    # opens the directory of the current render path
    def openfolder(self):
        path = bpy.data.scenes["Scene"].render.filepath
        subprocess.call("explorer " + path, shell=True)


    # sets target render path taken from the scene's render output and cleaned up as needed
    def SetOutputPath(self, node):
        defaultPath = bpy.context.scene.render.filepath
        dirname = os.path.dirname(defaultPath)
        if not dirname.endswith( ('/', '\\') ):
            dirname += "/"
        if not dirname:
            dirname = os.path.expanduser('~') + "/"
        fileName = "output"
        if bpy.app.version[0] >= 5:
            node.directory = dirname
            node.file_name = fileName
        else:
            node.base_path = dirname + fileName


    # creates a new Render Layers node at the given position
    def CreateNodeRenderLayers(self, position):
        nodeTree = self.GetNodeTree()
        node = nodeTree.nodes.new('CompositorNodeRLayers')
        node.location = position
        return node


    # creates a new Output File node at the given position
    def CreateNodeFileOutput(self, position):
        bpy.context.scene.render.image_settings.media_type = 'MULTI_LAYER_IMAGE'
        bpy.context.scene.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
        nodeTree = self.GetNodeTree()
        node = nodeTree.nodes.new("CompositorNodeOutputFile")
        node.label = 'EXR-MultiLayer'
        self.SetOutputPath(node)
        node.location = position
        node.width = 300
        node.use_custom_color = True
        node.color = (0.686, 0.204, 0.176)
        return node


    # links all outputs of the source node to inputs of the target node
    def LinkRenderLayers(self, sourceNode, targetNode):
        nodeTree = self.GetNodeTree()
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
                    nodeTree.links.new(out, targetNode.inputs[slot])
                    break
                slot = slot + 1
            if not found:
                # target node has no matching input, create one and link to it
                if bpy.app.version[0] >= 5:
                    socketType = out.type
                    if socketType == 'VALUE':
                        socketType = 'FLOAT'
                    targetNode.file_output_items.new(socketType, out.identifier)
                    nodeTree.links.new(out, targetNode.inputs[-2])
                else:
                    targetNode.file_slots.new(out.identifier)
                    nodeTree.links.new(out, targetNode.inputs[-1])


    # Exr Auto Saver button
    # Generates reqired nodes for the OpenEXR output and links available render passes
    def execute(self, context):
        scene = bpy.context.scene # get the scene

        #if not scene.use_nodes:
        if self.GetNodeTree() == None:
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

        row = layout.row()
        row.scale_y = 2.0
        row.operator(Exr_Auto_Pass_Saver.bl_idname, icon='TRACKING_FORWARDS')
        sce = context.scene

        layout.prop(sce, "exr_auto_pass_saver_clear_all") 
        layout.prop(sce, "exr_auto_pass_saver_open_dir") 

        layout.separator()
        box = layout.box()
        col = box.column(align=True)
        row = col.row()
        row.label(text="Our Other Tools", icon='INFO')
        col.separator(factor=0.5)

        row = col.row()
        row.label(text="Free EXR reader for PS", icon='BLANK1')
        row = col.row()
        row.scale_y = 1.2
        row.operator("wm.url_open", text="Exr-IO", icon="URL").url = "https://www.exr-io.com"
        col.separator(factor=0.3)

        row = col.row()
        row.label(text="Need auto unwrapping?", icon='BLANK1')
        row = col.row()
        row.scale_y = 1.2
        row.operator("wm.url_open", text="Unwrella", icon="URL").url = "https://www.unwrella.com"

classes = (Exr_Auto_Pass_Saver_Panel, Exr_Auto_Pass_Saver)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
