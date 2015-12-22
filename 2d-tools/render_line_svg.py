#!/usr/bin/python
# -*- coding: utf-8 -*-

BLACK = [0,0,0,1]

def order_edges(edges):
  res = []
  ev_dict = {}
  ve_dict = {}
  e_visited = {}
  v_ordered = []
  e_order = []
  enum = len(edges)

  for e,(v1,v2) in enumerate(edges):

    ev_dict[e] = [v1,v2]

    if v1 in ve_dict:
      ve_dict[v1].append(e)
    else:
      ve_dict[v1] = [e]

    if v2 in ve_dict:
      ve_dict[v2].append(e)
    else:
      ve_dict[v2] = [e]

  e_start = 0
  for v,ee in ve_dict.iteritems():
    if len(ee)<2:
      e_start = ee[0]
      break

  e_visited[e_start] = True

  vcurr = ev_dict[e_start][1]
  vend = ev_dict[e_start][0]

  v_ordered.append(vend)
  v_ordered.append(vcurr)
  e_order.append(e_start)

  while vend!=vcurr:

    try:

      if ve_dict[vcurr][0] in e_visited:
        e = ve_dict[vcurr][1]
      else:
        e = ve_dict[vcurr][0]

      e_visited[e] = True
      e_order.append(e)

      v1,v2 = ev_dict[e]

      if v1 == vcurr:
        vcurr = v2
      else:
        vcurr = v1

      v_ordered.append(vcurr)

    except Exception:
      break

  return e_order, v_ordered


def make_random_line(c, vertices, edges, n=10):

  from numpy import arange
  from numpy import array
  from numpy.random import random

  # e_order puts edges in successive order, but consecutuve edge vertices may
  # not have correct order. 
  # v_ordered contains the ordered vertices of the entire path.
  e_order,v_ordered = order_edges(edges)

  ## order edges, and get vertex coordinates
  # xys = vertices[edges[e_order]]

  xys = vertices[v_ordered,:]

  c.new_path()
  curr = xys[0,:]
  for xy in xys[1:,:]:

    dd = (xy-curr)*random()
    c.move_to(*curr)
    c.line_to(*(curr+dd))
    curr = xy
  
  c.stroke()

def make_line(c, vertices, edges, n=10):

  from numpy import arange
  from numpy import array

  # e_order puts edges in successive order, but consecutuve edge vertices may
  # not have correct order. 
  # v_ordered contains the ordered vertices of the entire path.
  e_order,v_ordered = order_edges(edges)

  ## order edges, and get vertex coordinates
  # xys = vertices[edges[e_order]]

  xys = vertices[v_ordered,:]

  c.new_path()
  curr = xys[0,:]
  c.move_to(*curr)
  for xy in xys[1:,:]:
    c.line_to(*xy)
  
  c.stroke()
  

def main(args, **argv):

  from dddUtils.ioOBJ import load_2d as load
  from cairo import SVGSurface, Context
  from numpy import array
  from glob import glob

  prefix = args.prefix
  size = args.size
  scale = args.scale
  one = 1.0/size
  steps = args.steps
  stride = args.stride
  skip = args.skip

  out = prefix + '.svg'
  print('making file: {:s}'.format(out))

  s = SVGSurface(out, size, size)
  c = Context(s)

  c.set_line_width(0.1)
  c.set_source_rgba(*BLACK)


  for fn in sorted(glob(prefix + '*.2obj'))[skip:steps:stride]:

    print(fn)

    data = load(fn)

    vertices = data['vertices']
    vertices *= scale*size
    edges = data['edges']
    # make_random_line(c, vertices, edges)
    make_line(c, vertices, edges)

  c.save()

  return

if __name__ == '__main__':

  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument(
    '--prefix',
    type=str,
    required=True
  )
  parser.add_argument(
    '--size',
    type=int,
    default=1000
  )
  parser.add_argument(
    '--steps',
    type=int,
    default=100000
  )
  parser.add_argument(
    '--stride',
    type=int,
    default=1
  )
  parser.add_argument(
    '--skip',
    type=int,
    default=0
  )
  parser.add_argument(
    '--scale',
    type=float,
    default=1.0
  )

  args = parser.parse_args()

  main(args)

