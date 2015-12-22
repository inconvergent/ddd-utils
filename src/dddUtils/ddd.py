# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function


def get_mid_2d(v):

  from numpy import array

  mi = v.min(axis=0).squeeze()
  ma = v.max(axis=0).squeeze()
  midx = mi[0]+ma[0]
  midy = mi[1]+ma[1]
  move = array([[midx,midy]])*0.5
  return move

def get_mid_3d(v):

  from numpy import array

  mi = v.min(axis=0).squeeze()
  ma = v.max(axis=0).squeeze()
  midx = mi[0]+ma[0]
  midy = mi[1]+ma[1]
  midz = mi[2]+ma[2]
  move = array([[midx,midy,midz]])*0.5
  return move

def random_unit_vec(num, scale):

  from numpy.random import normal
  from numpy.linalg import norm
  from numpy import reshape

  rnd = normal(size=(num,3))
  d = norm(rnd,axis=1)
  rnd[:] /= reshape(d, (num,1))
  return rnd*scale

def export_svg(fn, paths, size):

  from cairo import SVGSurface, Context
  from numpy import array

  one = 1.0/size
  s = SVGSurface(fn, size, size)
  c = Context(s)

  c.set_line_width(0.1)

  paths = spatial_sort(paths)

  for path in paths: 
    path *= size

    c.new_path()
    c.move_to(*path[0,:])
    for p in path[1:]:
      c.line_to(*p)
    c.stroke()


def random_points_in_circle(n, x, y, rad):
  """
  get n random points in a circle.
  """

  from numpy import zeros, logical_not
  from numpy import column_stack
  from numpy import cos
  from numpy import sin
  from numpy import array
  from numpy import pi
  from numpy import reshape
  from numpy.random import random

  rnd = random(size=(n,3))
  t = 2.*pi*rnd[:,0]
  u = rnd[:,1:].sum(axis=1)
  r = zeros(n,'float')
  mask = u>1.
  xmask = logical_not(mask)
  r[mask] = 2.-u[mask]
  r[xmask] = u[xmask]
  xyp = reshape(rad*r,(n,1))*column_stack( (cos(t),sin(t)) )
  dartsxy  = xyp + array([x,y])
  return dartsxy


def darts(n, x, y, rad, dst, old_darts=None):
  """
  get at most n random, uniformly distributed, points in a circle.
  centered at (x,y), with radius rr. points are no closer to each other
  than dst.
  """

  from numpy import array
  from numpy import zeros
  from numpy import row_stack 
  from scipy.spatial import cKDTree as kdt

  dartsxy = random_points_in_circle(n, x, y, rad)
  jj = zeros(n,'bool')

  tree = kdt(dartsxy)
  for j,near in enumerate(tree.query_ball_point(dartsxy, dst)):
    if len(near)<2:
      jj[j] = True

  res = dartsxy[jj,:]

  if old_darts is not None:
    return row_stack([old_darts, res])

  return res

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

def spatial_sort(paths, init_rad=0.01):

  from numpy import row_stack
  from numpy import array
  from numpy import zeros
  from numpy.linalg import norm
  from scipy.spatial import cKDTree as kdt

  num = len(paths)

  res = []

  unsorted = set(range(2*num))

  xs = zeros((2*num,2), 'float')
  x_path = zeros(2*num, 'int')

  for i, path in enumerate(paths):
    xs[i,:] = path[0,:]
    xs[num+i,:] = path[-1,:]

    x_path[i] = i
    x_path[num+i] = i

  tree = kdt(xs)

  count = 0
  pos = array([0,0],'float')

  while count<num:

    rad = init_rad
    while True:

      near = tree.query_ball_point(pos, rad)
      cands = list(set(near).intersection(unsorted))
      if not cands:
        rad *= 2.0
        continue

      dst = norm(pos - xs[cands,:], axis=1)
      cp = dst.argmin()
      uns = cands[cp]
      break

    path_ind = x_path[uns]
    path = paths[path_ind]

    if uns>=num:
      res.append(path[::-1])
      pos = paths[path_ind][0,:]
      unsorted.remove(uns)
      unsorted.remove(uns-num)

    else:
      res.append(path)
      pos = paths[path_ind][-1,:]
      unsorted.remove(uns)
      unsorted.remove(uns+num)

    count += 1

  return res

