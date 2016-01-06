# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

from numpy.random import random
from numpy.linalg import norm
from scipy.spatial import cKDTree as kdt
from numpy import column_stack
from numpy import row_stack
from numpy import zeros
from numpy import reshape
from numpy import logical_not
from numpy import logical_and
from numpy import array
from numpy import pi as PI
from numpy import cos
from numpy import sin


def random_unit_vec(num, scale):
  from numpy.random import normal

  rnd = normal(size=(num,3))
  d = norm(rnd,axis=1)
  rnd[:] /= reshape(d, (num,1))
  return rnd*scale

def random_points_in_circle(n,xx,yy,rr):
  """
  get n random points in a circle.
  """


  rnd = random(size=(n,3))
  t = 2.*PI*rnd[:,0]
  u = rnd[:,1:].sum(axis=1)
  r = zeros(n,'float')
  mask = u>1.
  xmask = logical_not(mask)
  r[mask] = 2.-u[mask]
  r[xmask] = u[xmask]
  xyp = reshape(rr*r,(n,1))*column_stack( (cos(t),sin(t)) )
  dartsxy  = xyp + array([xx,yy])
  return dartsxy

def random_points_in_rectangle(n, xx, yy, w, h):

  rnd = random((n,2))
  height_mask = logical_and(rnd[:,1]>yy-h*0.5, rnd[:,1]<yy+h*0.5)
  width_mask = logical_and(rnd[:,0]>xx-w*0.5, rnd[:,0]<xx+w*0.5)
  mask = logical_and(height_mask, width_mask)
  return rnd[mask,:]

def darts(n, xx, yy, rr, dst):
  """
  get at most n random, uniformly distributed, points in a circle.
  centered at (xx,yy), with radius rr. points are no closer to each other
  than dst.
  """

  ## remove new nodes that are too close to other
  ## new nodes

  visited = set()
  dartsxy = random_points_in_circle(n, xx, yy, rr)
  tree = kdt(dartsxy)
  near = tree.query_ball_point(dartsxy, dst)
  jj = []
  for j,n in enumerate(near):

    if len(visited.intersection(n))<1:
      jj.append(j)
      visited.add(j)

  res = dartsxy[jj,:]
  return res

def darts_rect(n, xx, yy, w=1, h=1, dst=0):


  ## remove new nodes that are too close to other
  ## new nodes

  visited = set()
  dartsxy = random_points_in_rectangle(n, xx, yy, w, h)
  tree = kdt(dartsxy)
  near = tree.query_ball_point(dartsxy, dst)
  jj = []
  for j,n in enumerate(near):

    if len(visited.intersection(n))<1:
      jj.append(j)
      visited.add(j)

  res = dartsxy[jj,:]
  return res



