bl_info = {
    "name" : "Lazy Rename",
    "description" : "Rename objects in conformity of Lazy Builder's data format",
    "author" : "Guilherme Gama",
    "version" : (0, 0, 1),
    "blender" : (2, 80, 0),
    "location" : "View3D",
    "warning" : "",
    "support" : "COMMUNITY",
    "doc_url" : "",
    "category" : "3D View"
}

import bpy

from bpy.types import Operator
from bpy.props import StringProperty
from bpy.types import Panel


# Execution Blocks

class RENAMER_OT_Message(Operator):
    """ Rename objects in conformity of Lazy Builder's data format
    """
    bl_idname = "lazy.rename"
    bl_label = "LazyRename"
    bl_description = "Rename objects in conformity of Lazy Builder's data format"
    bl_options = {"REGISTER"}
    
    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"
    
    def execute(self, context):
        if not context.active_object:
           self.report({'ERROR'}, "No object selected")
           return {'CANCELLED'}
        if len(context.selected_objects) != 1:
           self.report({'ERROR'}, "Select only one object at a time")
           return {'CANCELLED'}
        name = context.active_object.name
        context.active_object.name = context.object.item+"_"+context.object.itemType
        context.active_object.data.name = context.object.item+"_"+context.object.itemType
        return {'FINISHED'}
    
    
class IMPORT_OT_Message(Operator):
    """ Import named objects in conformity of Lazy Builder's data format
    """
    bl_idname = "lazy.import"
    bl_label = "LazyImport"
    bl_description = "Import named objects in conformity of Lazy Builder's data format"
    bl_options = {"REGISTER"}
    
    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"
    
    def execute(self, context):
        if not context.active_object:
           self.report({'ERROR'}, "No object selected")
           return {'CANCELLED'}
        if len(context.selected_objects) != 1:
           self.report({'ERROR'}, "Select only one object at a time")
           return {'CANCELLED'}
       
        splited=context.active_object.name.split("_")
        context.object.item= splited[0]
        context.object.itemType= splited[1]
        return {'FINISHED'}

class RENAMECOL_OT_Message(Operator):
    """ Import named objects in conformity of Lazy Builder's data format
    """
    bl_idname = "lazy.renamecol"
    bl_label = "LazyRenameCol"
    bl_description = "Rename the collection of the current selected object"
    bl_options = {"REGISTER"}
    
    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"
    
    def execute(self, context):
        if not context.active_object:
           self.report({'ERROR'}, "No object selected")
           return {'CANCELLED'}
        
        if len(bpy.context.active_object.users_collection) == 0 :
            self.report({'ERROR'}, "No collection grouping this object")
            return {'CANCELLED'}
       
        bpy.context.active_object.users_collection[0].name= context.object.item+"_"+context.object.itemType
        
        for obj in bpy.context.active_object.users_collection[0].all_objects :
            obj.item = context.object.item
            obj.itemType = context.object.itemType
        

        return {'FINISHED'}
    
# Display Blocks
    
class RENAMER_PT_Panel(Panel):
    """ The renaming panel
    """
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Lazy Rename"
    bl_idname = "lazyrenamer.panel"
    bl_label = "Lazy Rename"
    
    def draw(self, context):
        col = self.layout.column()
        col.prop(context.object, "item", text = "Item")
        col.prop(context.object, "itemType", text = "Type")
        col.operator("lazy.import", text="Import")
        col.operator("lazy.rename", text="Rename Object")
        col.operator("lazy.renamecol", text="Rename Collection")

        
classes = [
    RENAMER_OT_Message,
    RENAMECOL_OT_Message,
    RENAMER_PT_Panel,
    IMPORT_OT_Message,
]



# Main Blocks

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Object.item= bpy.props.StringProperty(
        name="Item",
        description="Item name",
        default="",
    )
    
    bpy.types.Object.itemType= bpy.props.StringProperty(
        name="Item Type",
        description="Item Type Name",
        default="",
    )
    
    
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Object.suffix
    
if __name__ == '__main__':
    register()