# -*- coding: utf-8 -*-

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

