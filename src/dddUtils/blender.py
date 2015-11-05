# -*- coding: utf-8 -*-

import bpy

class Base(object):

  def __init__(self, fn, obj_name):

    self.fn = fn
    self.obj_name = obj_name

    return

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

  def move_rescale(self, pos, scale):

    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')

    obj = self.obj

    sx,sy,sz = obj.scale

    sx *= scale
    sy *= scale
    sz *= scale

    obj.scale = ((sx,sy,sz))

  def smooth(self, view_levels=1, render_levels=2):

    bpy.context.scene.objects.active = self.obj

    bpy.ops.object.modifier_add(type='SUBSURF')
    self.obj.modifiers['Subsurf'].levels = view_levels
    self.obj.modifiers['Subsurf'].render_levels = render_levels

    bpy.ops.object.shade_smooth()

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

  def apply_mat(self):

    mat = bpy.data.materials["Material"]
    self.obj.data.materials.append(mat)

class Obj(Base):

  def __init__(self, fn, obj_name):

    Base.__init__(self, fn, obj_name)
    self.obj = self.__import(fn)

  def __import(self, fn):

    bpy.ops.object.select_all(action='DESELECT')

    bpy.ops.import_scene.obj(
      filepath=fn,
      use_smooth_groups=False,
      use_edges=True,
    )

    obj = bpy.context.selected_objects[0]

    return obj

#class CloudObj(object):

  #def __init__(self, fn, obj_name):

    #self.fn = fn
    #self.obj_name = obj_name
    #self.obj = self.__import(fn)

    #return

  #def __import(self, fn):

    #bpy.ops.object.select_all(action='DESELECT')

    #bpy.ops.import_scene.obj(
      #filepath=fn,
      #use_smooth_groups=False,
      #use_edges=True,
    #)

    #obj = bpy.context.selected_objects[0]

    #return obj


  #def del_mesh(self):

    #bpy.ops.object.select_all(action='DESELECT')
    #self.obj.select=True
    #bpy.ops.object.delete()

  #def spheres(self):

    #from numpy import array
    #from numpy import row_stack
    #from numpy import diff
    #from numpy import mean
    #from numpy.linalg import norm
    #from collections import defaultdict

    #base_scale = 0.65

    #scn = bpy.context.scene
    #obj = self.obj
    #world = obj.matrix_world
    #mat = bpy.data.materials["Material"]


    #bpy.ops.surface.primitive_nurbs_surface_sphere_add(
      #radius = 1,
      #location = (0,0,0)
    #)
    #sphere = bpy.context.active_object
    #sphere.data.materials.append(mat)
    #bpy.context.active_object.hide = True
    #bpy.context.active_object.hide_render = True

    #mesh = sphere.data

    #vertex_map = defaultdict(list)
    #vertices = obj.data.vertices
    #edges = obj.data.edges
    #vnum = len(vertices)
    #enum = len(edges)
    #vert_co = row_stack([world*v.co for v in vertices])

    #print('\ncalculating sizes:\n')

    #for i,e in enumerate(edges):

      #vv = array([v for v in e.vertices],'int')
      #dx = diff(vert_co[vv,:],axis=0).squeeze()
      ##dx = diff(row_stack([ \for v in vv]),axis=0).squeeze()
      #dd = norm(dx)

      #vertex_map[vv[0]].append(dd)
      #vertex_map[vv[1]].append(dd)

      #if i%100==0:
        #print(i, enum)

    #vertex_weight = {k:mean(d) for k,d in vertex_map.items()}

    #print('\nplacing objects:\n')

    #for i,(v,rad) in enumerate(vertex_weight.items()):

      #o = bpy.data.objects.new('one', mesh)
      ##o.location = world*vertices[v].co
      #o.location = vert_co[v,:]

      #scale = rad*base_scale

      #sx,sy,sz = o.scale
      #sx *= scale
      #sy *= scale
      #sz *= scale

      #o.scale = ((sx,sy,sz))
      #scn.objects.link(o)

      #if i%100==0:
        #print(i, vnum)



