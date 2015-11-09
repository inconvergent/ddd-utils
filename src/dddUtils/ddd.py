# -*- coding: utf-8 -*-

def get_mid_2d(v):

  from numpy import array

  mi = v.min(axis=0).squeeze()
  ma = v.max(axis=0).squeeze()
  midx = (mi[0]+ma[0])*0.5
  midy = (mi[1]+ma[1])*0.5
  move = array([[midx,midy]])
  return move

def random_unit_vec(num, scale):

  from numpy.random import normal
  from numpy.linalg import norm
  from numpy import reshape

  rnd = normal(size=(num,3))
  d = norm(rnd,axis=1)
  rnd[:] /= reshape(d, (num,1))
  return rnd*scale

