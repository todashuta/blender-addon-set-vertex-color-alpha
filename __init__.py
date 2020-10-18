bl_info = {
    "name": "Set Vertex Color Alpha",
    "author": "todashuta",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Side Bar > Paint",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "https://github.com/todashuta/blender-addon-set-vertex-color-alpha/issues",
    "category": "Paint"
}


if "bpy" in locals():
    import importlib
    importlib.reload(set_vertex_color_alpha)
else:
    from . import set_vertex_color_alpha


import bpy


def register():
    set_vertex_color_alpha.register()


def unregister():
    set_vertex_color_alpha.unregister()


if __name__ == "__main__":
    register()
