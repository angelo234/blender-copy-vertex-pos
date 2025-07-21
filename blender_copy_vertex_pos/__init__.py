# Copyright (c) 2025 Angelo Matteo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

bl_info = {
    "name":        "Copy Vertex Position to Clipboard",
    "description": "Copy world-space position of the selected vertices to the clipboard",
    "author":      "angelo234",
    "version":     (0, 0, 1),
    "blender":     (4, 5, 0),
    "category":    "Mesh",
}

import bpy
import bmesh


class COPY_VERTEX_POS_OT_copy_vertex_pos(bpy.types.Operator):
    """Copy the world-space position of the selected vertices to the clipboard"""
    bl_idname = "copy_vertex_pos.copy_vertex_pos"
    bl_label = "Copy Selected Vertex Position(s) to Clipboard"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.edit_object
        if not obj or obj.type != 'MESH':
            return False

        bm = bmesh.from_edit_mesh(obj.data)
        sel = [v for v in bm.verts if v.select]
        if not sel:
            return False

        return True

    def execute(self, context):
        obj = context.edit_object
        bm = bmesh.from_edit_mesh(obj.data)
        sel = [v for v in bm.verts if v.select]

        if len(sel) == 1:
            v = sel[0]
            co_world = obj.matrix_world @ v.co
            coord_str = f"{co_world.x:.4f}, {co_world.y:.4f}, {co_world.z:.4f}"
            context.window_manager.clipboard = coord_str
            self.report({'INFO'}, f"Copied 1 vertex position to clipboard")
            return {'FINISHED'}

        else:
            coords = []
            for v in sel:
                co_world = obj.matrix_world @ v.co
                coords.append(f"{co_world.x:.4f}, {co_world.y:.4f}, {co_world.z:.4f}")

            coord_str = "\n".join(coords)
            context.window_manager.clipboard = coord_str

            self.report({'INFO'}, f"Copied {len(sel)} vertex positions to clipboard")
            return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(COPY_VERTEX_POS_OT_copy_vertex_pos.bl_idname, icon='COPYDOWN')


def register():
    bpy.utils.register_class(COPY_VERTEX_POS_OT_copy_vertex_pos)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_func)
    bpy.utils.unregister_class(COPY_VERTEX_POS_OT_copy_vertex_pos)


if __name__ == "__main__":
    register()