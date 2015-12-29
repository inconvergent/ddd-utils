# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

from numpy.random import normal
from numpy.random import random


def random_unit_vec(num, scale):

  from numpy.linalg import norm
  from numpy import reshape

  rnd = normal(size=(num,3))
  d = norm(rnd,axis=1)
  rnd[:] /= reshape(d, (num,1))
  return rnd*scale

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

