import bpy


def set_vertex_color_alpha(context, alpha_vaule):
    obj = context.active_object
    selected_verts = [v for v in obj.data.vertices if v.select]
    mesh = obj.data
    color_layer = mesh.vertex_colors.active

    for polygon in mesh.polygons:
        for selected_vert in selected_verts:
            for i, index in enumerate(polygon.vertices):
                if selected_vert.index == index:
                    loop_index = polygon.loop_indices[i]
                    color_layer.data[loop_index].color[3] = alpha_vaule



def set_face_vertex_color_alpha(context, alpha_vaule):
    obj = context.active_object
    mesh = obj.data
    color_layer = mesh.vertex_colors.active

    i = 0
    for poly in mesh.polygons:
        for _ in poly.loop_indices:
            if poly.select:
                color_layer.data[i].color[3] = alpha_vaule
            i += 1


def set_all_face_vertex_color_alpha(context, alpha_vaule):
    obj = context.active_object
    mesh = obj.data
    color_layer = mesh.vertex_colors.active

    i = 0
    for poly in mesh.polygons:
        for _ in poly.loop_indices:
            color_layer.data[i].color[3] = alpha_vaule
            i += 1


def _poll(context):
    ob = context.active_object
    return ob is not None and ob.type == 'MESH' and ob.mode == 'VERTEX_PAINT'


def main(context, alpha_vaule):
    assert _poll(context), "Invalid Context"

    obj = context.active_object
    mesh = obj.data
    if mesh.use_paint_mask:
        set_face_vertex_color_alpha(context, alpha_vaule)
    elif mesh.use_paint_mask_vertex:
        set_vertex_color_alpha(context, alpha_vaule)
    else:
        set_all_face_vertex_color_alpha(context, alpha_vaule)


class SET_VERTEX_COLOR_ALPHA_OT_main(bpy.types.Operator):
    bl_idname = "object.set_vertex_color_alpha"
    bl_label = "Set Vertex Color Alpha"
    bl_options = {"REGISTER", "UNDO"}

    alpha: bpy.props.FloatProperty(
        name="Alpha",
        min=0.0,
        max=1.0,
        default=0.0,
    )

    @classmethod
    def poll(cls, context):
        return _poll(context)

    def execute(self, context):
        main(context, self.alpha)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.alpha = context.scene.set_vertex_color_alpha_alpha_value
        return self.execute(context)


class SET_VERTEX_COLOR_ALPHA_PT_panel(bpy.types.Panel):
    bl_label = "Vertex Color Alpha"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Paint"

    @classmethod
    def poll(self, context):
        return _poll(context)

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.prop(scene, "set_vertex_color_alpha_alpha_value")
        layout.operator(SET_VERTEX_COLOR_ALPHA_OT_main.bl_idname)


classes = (
        SET_VERTEX_COLOR_ALPHA_OT_main,
        SET_VERTEX_COLOR_ALPHA_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.set_vertex_color_alpha_alpha_value = bpy.props.FloatProperty(
            name="Alpha", default=0.0, min=0.0, max=1.0, description="Vertex Color Alpha")


def unregister():
    if hasattr(bpy.types.Scene, "set_vertex_color_alpha_alpha_value"):
        del bpy.types.Scene.set_vertex_color_alpha_alpha_value

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
