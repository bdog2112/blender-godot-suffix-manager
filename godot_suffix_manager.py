# SUFFIX MANAGER FOR GODOT
# Convient tool for adding Godot import suffixes to object names in Blender.
#
# HOW IT WORKS
# User selects 1 or more objects, selects a suffix and presses the
# "Add" button. Tool removes any existing suffixes and adds the new
# suffix.
# Alternatively, user selects 1 or more objects and presses the
# "Remove button. Tool removes any existing suffixes.
# When ready, user presses "Export GLTF" button to open Blender's
# GLTF export screen.
#
# TODO
# - Remove any references to "collisions" and focus on suffixes.
# - Expand suffix descriptions with a little more detail
#
# VERSION HISTORY
# v1.0
# Creates a "Suffix Manager" panel in 3D Viewport > Sidebar.
# Provides list of Godot import suffixes and brief descriptions.
# Provides ability to Add/Remove suffixes to selected objects.
# Includes convenient "Export GLTF" button.

bl_info = {
    "name": "Godot Suffix Manager",
    "author": "Bdog",
    "version": (1, 0),
    "blender": (3, 6, 1),
    "location": "3D Viewport > Sidebar > Suffix Manager",
    "description": "Helps prep object names for export to Godot",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}


import bpy


class SuffixTools():
    suffix_list = [
        ('noimp', "-noimp", "Don't import"),
        ('col', "-col", "Add collision"),  # Default selection
        ('colonly', "-colonly", "Drop mesh and add collision"),
        ('convcol', "-convcol", "Add convex collision"),
        ('convcolonly', "-convcolonly", "Drop mesh and add convex collision"),
        ('occ', "-occ", "Add occluder"),
        ('occonly', "-occonly", "Add occluder only"),
#        ('multimesh', "-multimesh", "Drop mesh and add multimesh"),
        ('navmesh', "-navmesh", "Drop mesh and add navmesh"),
        ('vehicle', "-vehicle", "Add vehiclebody with mesh as child"),
        ('wheel', "-wheel", "Add vehiclewheel with mesh as child"),
        ('rigid', "-rigid", "Add rigidbody"),
        ('loop', "-loop", "Add looping animation"),
        ('cycle', "-cycle", "Add looping animation"),
    ]
    
    def add_suffix(self, operator, context):
        print('\nADD SUFFIX:')
        # Get the currently selected suffix
        suffix = "-" + context.scene.suffix_prop.suffix_type
        suf_len = len(suffix)
        for obj in context.selected_objects:
            obj_suf = self.get_suffix(obj.name)
            # Continue to next object if suffix match
            if obj_suf == suffix:
                continue
            # Remove existing suffix
            elif obj_suf != None:
                self.remove_single_suffix(obj, obj_suf)
            # Add new suffix
            new_name = obj.name + suffix
            obj.name = new_name
            print("New name: ", obj.name)
    
    def remove_suffixes(self, operator, context):
        print('\nREMOVE SUFFIX:')
        # Iterate list of selected objects
        for obj in context.selected_objects:
            # Iterate list of suffixes
            for suffix_row in SuffixTools.suffix_list:
                suffix = suffix_row[1]
                self.remove_single_suffix(obj, suffix)
    
    def remove_single_suffix(self, obj, suffix):
        suf_len = len(suffix)
        end_of_name = obj.name[-suf_len:]
        if end_of_name == suffix:
            new_name = obj.name[:-suf_len]
            obj.name = new_name
            print("New name: ", obj.name)
    
    def get_suffix(self, obj_name):
        # Iterate suffix list and compare to object name. If end of
        # object name contains a matching suffix, then return that
        # suffix.
        for suffix_row in self.suffix_list:
            suffix = suffix_row[1]
            suf_len = len(suffix)
            end_of_name = obj_name[-suf_len:]
            if end_of_name == suffix:
                return suffix
        return None


class AddSuffix(bpy.types.Operator):
    """Add suffix to object names""" # Button tooltip
    bl_idname = "object.operator_add_suffix"
    bl_label = "Add" # Button text

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        suffix_tools = bpy.types.Scene.suffix_tools
        suffix_tools.add_suffix(self, context)
        return {'FINISHED'}


class RemoveSuffix(bpy.types.Operator):
    """Remove suffix from object names""" # Button tooltip
    bl_idname = "object.operator_remove_suffix"
    bl_label = "Remove" # Button text

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        suffix_tools = bpy.types.Scene.suffix_tools
        suffix_tools.remove_suffixes(self, context)
        return {'FINISHED'}


class ExportGLTF(bpy.types.Operator):
    """Open GLTF export screen"""
    bl_idname = "object.operator_export_gltf"
    bl_label = "Export GLTF"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        print('\nEXPORT GLTF:')
        bpy.ops.export_scene.gltf('INVOKE_SCREEN')
        return {'FINISHED'}


class SuffixTypeProp(bpy.types.PropertyGroup):
    suffix_type: bpy.props.EnumProperty(
        name="Suffix",
        description="List of Godot object import suffixes",
        items=SuffixTools.suffix_list,
        default='col'
    )


class LayoutSuffixManagerPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Suffix Manager for Godot"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Suffix Manager"

    def draw(self, context):
        layout = self.layout #UILayout struct

        scene = context.scene

         # Add collision renamer buttons
        layout.label(text="Manage selected objects:")
        row = layout.row()
        row.prop(scene.suffix_prop, "suffix_type")
        row = layout.row()
        row.operator("object.operator_add_suffix")
        row.operator("object.operator_remove_suffix")
        row = layout.row()
        row.operator("object.operator_export_gltf")

def register():
    bpy.types.Scene.suffix_tools = SuffixTools()
    bpy.utils.register_class(AddSuffix)
    bpy.utils.register_class(RemoveSuffix)
    bpy.utils.register_class(ExportGLTF)
    bpy.utils.register_class(LayoutSuffixManagerPanel)
    bpy.utils.register_class(SuffixTypeProp)
    bpy.types.Scene.suffix_prop = bpy.props.PointerProperty(type=SuffixTypeProp)


def unregister():
    del bpy.types.Scene.suffix_prop
    bpy.utils.unregister_class(SuffixTypeProp)
    bpy.utils.unregister_class(LayoutSuffixManagerPanel)
    bpy.utils.unregister_class(ExportGLTF)
    bpy.utils.unregister_class(RemoveSuffix)
    bpy.utils.unregister_class(AddSuffix)
    del bpy.types.Scene.suffix_tools


if __name__ == "__main__":
    register()
