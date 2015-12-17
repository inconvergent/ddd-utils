#!/usr/bin/python
# -*- coding: utf-8 -*-

BLACK = [0,0,0,1]


def get_mid(v):

  from numpy import array

  mi = v.min(axis=0).squeeze()
  ma = v.max(axis=0).squeeze()
  midx = (mi[0]+ma[0])*0.5
  midy = (mi[1]+ma[1])*0.5
  move = array([[midx,midy]])
  return move

def make_triangles(c, vertices, faces, edges):

  hit_edges = set()
  hits = 0
  edges = 0

  for v1,v2,v3 in faces:

    for e in [
        tuple(sorted([v1,v2])), 
        tuple(sorted([v2,v3])), 
        tuple(sorted([v3,v1]))
    ]:

      if e not in hit_edges:

        c.move_to(*vertices[e[0]])
        c.line_to(*vertices[e[1]])
        # c.close_path()
        c.stroke()

        hit_edges.add(e)
        edges += 1

      else:
        hits += 1

  print('edges', edges)
  print('hits', hits)

  return

def make_random_stripes(c, vertices, faces, edges, n=10):

  from numpy import arange
  from numpy.random import random
  from numpy import roll

  rolls = 3
  xys = vertices[faces]

  ii = arange(n)/float(n)
  print(ii)

  for xy in xys:

    for r in [roll(arange(rolls),r) for r in range(3)]:

      va = xy[r[0],:]
      vb = xy[r[1],:]
      vc = xy[r[2],:]
      
      v1 = va-vc
      v2 = vb-vc

      for i in ii:
        if random()<0.3:
          continue

        c.move_to(*(va - i*v1))
        c.line_to(*(vb - i*v2))

      c.stroke()

  return

def make_random_length_strips(c, vertices, faces, edges, n=10):

  from numpy import arange
  from numpy.random import random
  from numpy import roll

  rolls = 3
  xys = vertices[faces]

  ii = arange(n)/float(n)
  print(ii)

  for xy in xys:

    va = xy[0,:]
    vb = xy[1,:]
    vc = xy[2,:]
    
    v1 = va-vc
    v2 = vb-vc

    for i in ii:

      start = va - i*v1
      stop = vb - i*v2
      dd = (stop-start)*random()

      c.move_to(*start)
      c.line_to(*start+dd)

    c.stroke()

  return

def main(args, **argv):

  # from render.render import Render
  from dddUtils.ioOBJ import load_2d as load
  from cairo import SVGSurface, Context
  from numpy import array

  size = args.size
  scale = args.scale
  one = 1.0/size

  data = load(args.fn)
  print(data)

  vertices = data['vertices']
  faces = data['faces']
  edges = data['edges']

  out = '.'.join(args.fn.split('.')[:-1])+'.svg'
  print('making file: {:s}'.format(out))

  s = SVGSurface(out, size, size)
  c = Context(s)

  c.set_line_width(0.1)
  c.set_source_rgba(*BLACK)

  vertices -= get_mid(vertices)
  vertices *= scale
  vertices += array([[0.5,0.5]])
  vertices *= size

  make_triangles(c, vertices, faces, edges)
  # make_random_length_strips(c, vertices, faces, edges)

  c.save()

  return

if __name__ == '__main__':

  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument(
    '--fn',
    type=str,
    required=True
  )
  parser.add_argument(
    '--rad',
    type=float,
    default=1
  )
  parser.add_argument(
    '--size',
    type=int,
    default=1000
  )
  parser.add_argument(
    '--alpha',
    type=float,
    default=1.0
  )
  parser.add_argument(
    '--scale',
    type=float,
    default=1.0
  )

  args = parser.parse_args()

  main(args)

