bl_info = {
    "name": "Sum Edge Length",
    "blender": (4, 0, 2),
    "category": "3D View",
    "author": "Jacob Beatty",
}

import bpy
import bmesh

class MESH_OT_sum_edge_length(bpy.types.Operator):
    bl_idname = "mesh.sum_edge_length"
    bl_label = "Sum Edge Length"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "No mesh object selected")
            return {'CANCELLED'}

        bm = bmesh.from_edit_mesh(obj.data)
        total_length = sum(e.calc_length() for e in bm.edges if e.select)
        
        context.workspace.status_text_set(f"Total Edge Length: {total_length:.2f}")
        self.report({'INFO'}, f"Total Edge Length: {total_length:.2f}")
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(MESH_OT_sum_edge_length.bl_idname)

def register():
    bpy.utils.register_class(MESH_OT_sum_edge_length)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(menu_func)

def unregister():
    bpy.utils.unregister_class(MESH_OT_sum_edge_length)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_func)

if __name__ == "__main__":
    register()