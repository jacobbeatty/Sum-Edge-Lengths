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
        
        # Adjust for unit scale
        unit_settings = context.scene.unit_settings
        unit_scale = unit_settings.scale_length
        total_length *= unit_scale
        
        # Convert to the appropriate unit
        if unit_settings.length_unit == 'METERS':
            unit_length = 'm'
        elif unit_settings.length_unit == 'CENTIMETERS':
            total_length *= 100
            unit_length = 'cm'
        elif unit_settings.length_unit == 'MILLIMETERS':
            total_length *= 1000
            unit_length = 'mm'
        elif unit_settings.length_unit == 'KILOMETERS':
            total_length /= 1000
            unit_length = 'km'
        elif unit_settings.length_unit == 'INCHES':
            total_length *= 39.3701
            unit_length = 'in'
        elif unit_settings.length_unit == 'FEET':
            total_length *= 3.28084
            unit_length = 'ft'
        elif unit_settings.length_unit == 'MILES':
            total_length /= 1609.34
            unit_length = 'mi'
        else:
            unit_length = 'm'  # Default to meters if unit is unknown
        
        context.workspace.status_text_set(f"Total Edge Length: {total_length:.3f} {unit_length}")
        self.report({'INFO'}, f"Total Edge Length: {total_length:.3f} {unit_length}")
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