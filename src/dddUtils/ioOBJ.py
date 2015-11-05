# -*- coding: utf-8 -*-

def load(fn):

  from codecs import open
  from numpy import row_stack

  vertices = []
  faces = []

  with open(fn, 'r', encoding='utf8') as f:

    for l in f:
      if l.startswith('#'):
        continue

      values = l.split()
      if not values:
        continue
      if values[0] == 'v':
        vertices.append([float(v) for v in values[1:]])

      if values[0] == 'f':
        face = [int(v.split('//')[0])-1 for v in values[1:]]
        faces.append(face)

  try:
    faces = row_stack(faces)
  except ValueError:
    faces = None

  return {
    'faces': faces,
    'vertices': row_stack(vertices)
  }

def load_to_centre(
  fn,
  sx=[1.0,1.0,1.0],
  mx=[0,5,0.5,0.5]
):

  from codecs import open
  from numpy import row_stack

  vertices = []
  faces = []

  with open(fn, 'r', encoding='utf8') as f:

    for l in f:
      if l.startswith('#'):
        continue

      values = l.split()
      if not values:
        continue
      if values[0] == 'v':
        vertices.append([float(v) for v in values[1:]])

      if values[0] == 'f':
        face = [int(v.split('//')[0])-1 for v in values[1:]]
        faces.append(face)

  np_vertices = row_stack(vertices)

  xmax = np_vertices[:,0].max()
  xmin = np_vertices[:,0].min()
  ymax = np_vertices[:,1].max()
  ymin = np_vertices[:,1].min()
  zmax = np_vertices[:,2].max()
  zmin = np_vertices[:,2].min()
  dx = xmax - xmin
  dy = ymax - ymin
  dz = zmax - zmin

  print('original')
  print('x min max, {:0.8f} {:0.8f}, dst: {:0.8f}'.format(xmin,xmax,dx))
  print('y min max, {:0.8f} {:0.8f}, dst: {:0.8f}'.format(ymin,ymax,dy))
  print('z min max, {:0.8f} {:0.8f}, dst: {:0.8f}'.format(zmin,zmax,dz))

  np_vertices /= max([dx,dy,dz])

  np_vertices[:,0] *= sx[0]
  np_vertices[:,1] *= sx[1]
  np_vertices[:,2] *= sx[2]

  np_vertices[:,0] += mx[0]
  np_vertices[:,1] += mx[1]
  np_vertices[:,2] += mx[2]

  xmax = np_vertices[:,0].max()
  xmin = np_vertices[:,0].min()
  ymax = np_vertices[:,1].max()
  ymin = np_vertices[:,1].min()
  zmax = np_vertices[:,2].max()
  zmin = np_vertices[:,2].min()
  dx = xmax - xmin
  dy = ymax - ymin
  dz = zmax - zmin

  print('rescaled')
  print('x min max, {:0.8f} {:0.8f}, dst: {:0.8f}'.format(xmin,xmax,dx))
  print('y min max, {:0.8f} {:0.8f}, dst: {:0.8f}'.format(ymin,ymax,dy))
  print('z min max, {:0.8f} {:0.8f}, dst: {:0.8f}'.format(zmin,zmax,dz))

  return {
    'faces': row_stack(faces),
    'vertices': np_vertices
  }

def export(obj_name, fn, verts, tris=None, meta=False):

  from codecs import open

  vnum = len(verts)

  if tris is not None:
    fnum = len(tris)
  else:
    fnum = 0

  print('storing mesh ...')
  print('num vertices: {:d}, num triangles: {:d}'.format(vnum, fnum))

  with open(fn, 'wb', encoding='utf8') as f:

    if meta:
      f.write('# meta:\n')
      f.write(meta+'\n')

    f.write('# info:\n')

    f.write('# vnum: {:d}\n# fnum: {:d}\n\n\n'
      .format(vnum, fnum))

    f.write('o {:s}\n'.format(obj_name))

    for v in verts:
      f.write('v {:f} {:f} {:f}\n'.format(*v))

    f.write('s off\n')

    if tris is not None:
      for t in tris:
        t += 1
        f.write('f {:d} {:d} {:d}\n'.format(*t))

    print('done.')

