# -*- coding: utf-8 -*-

import bpy

class Base(object):

  def __init__(self, fn, obj_name):

    self.fn = fn
    self.obj_name = obj_name
    self.obj = self._import(fn)

    return

  def _import(self, fn):

    bpy.ops.object.select_all(action='DESELECT')

    bpy.ops.import_scene.obj(
      filepath=fn,
      use_smooth_groups=False,
      use_edges=True,
    )

    obj = bpy.context.selected_objects[0]

    return obj

  def get_vertex_color(self):

    from mathutils import Color

    colors = []

    try:

      with open(self.fn+'.x', 'r', encoding='utf8') as f:

        for l in f:
          if l.startswith('#'):
            continue

          values = l.split()
          if not values:
            continue

          if values[0] == 'c':
            c = [float(v) for v in values[1:]]
            colors.append(c)

    except FileNotFoundError:
      return

    mesh = self.obj.data

    if not mesh.vertex_colors:
      mesh.vertex_colors.new()

    col = mesh.vertex_colors.active

    num = len(colors)

    numv = len(self.obj.data.polygons)

    i = 0

    for poly in self.obj.data.polygons:
      loop = poly.loop_indices
      verts = poly.vertices
      for idx,v in zip(loop,verts):
        col.data[idx].color = Color(colors[v])
        i += 1

    print(num, numv, len(col.data), i)

  def move_rescale(self, set_pivot=False, pos=False, scale=False, to_origin=False):

    obj = self.obj

    if set_pivot:
      bpy.context.scene.cursor_location = set_pivot
      bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

    if to_origin:
      bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')

    elif pos:
      mx,my,mz = obj.location

      mx = pos[0]
      my = pos[1]
      mz = pos[2]
      obj.location = ((mx,my,mz))

    if scale:
      sx,sy,sz = obj.scale
      sx *= scale
      sy *= scale
      sz *= scale
      obj.scale = ((sx,sy,sz))

  def set_smooth_shade(self):

    bpy.ops.object.shade_smooth()

  def smooth(self, view_levels=1, render_levels=2):

    bpy.context.scene.objects.active = self.obj

    bpy.ops.object.modifier_add(type='SUBSURF')
    self.obj.modifiers['Subsurf'].levels = view_levels
    self.obj.modifiers['Subsurf'].render_levels = render_levels

  def __set_vis(self, frame, vis=True):

    bpy.context.scene.objects.active = self.obj

    bpy.data.scenes['Scene'].frame_current = frame
    bpy.context.active_object.hide = not vis
    bpy.context.active_object.hide_render = not vis

    bpy.context.active_object.keyframe_insert(
      data_path="hide",
      index=-1,
      frame=frame
    )
    bpy.context.active_object.keyframe_insert(
      data_path="hide_render",
      index=-1,
      frame=frame
    )

  def animate_vis(self, ain, aout):

    self.__set_vis(0, False)
    self.__set_vis(ain, True)
    self.__set_vis(aout, False)

  def apply_mat(self, name='Material'):

    mat = bpy.data.materials[name]
    self.obj.data.materials.append(mat)

class Obj(Base):

  def __init__(self, fn, obj_name):

    Base.__init__(self, fn, obj_name)


class Cloud(Base):

  def __init__(self, fn, obj_name):

    Base.__init__(self, fn, obj_name)

  def spheres(self, scale=0.5, mat='Material'):

    #from numpy import row_stack
    #scn = bpy.context.scene
    #world = obj.matrix_world

    obj = self.obj
    mat = bpy.data.materials[mat]

    bpy.ops.surface.primitive_nurbs_surface_sphere_add(
      radius = 1,
      location = (0,0,0)
    )
    sphere = bpy.context.active_object

    sx,sy,sz = sphere.scale
    sx *= scale
    sy *= scale
    sz *= scale

    sphere.scale = ((sx,sy,sz))

    sphere.data.materials.append(mat)

    sphere.parent = obj

    obj.dupli_type = 'VERTS'

