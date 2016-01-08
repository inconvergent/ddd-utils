#!/usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import print_function
from __future__ import division

from collections import defaultdict
from itertools import product
from itertools import repeat
from operator import itemgetter

from numpy.random import randint
from numpy.linalg import norm

from scipy.spatial.distance import cdist
from numpy import mean
from numpy import ceil
from numpy import sqrt
from numpy import linspace
from numpy import meshgrid
from numpy import column_stack
from numpy import concatenate
from numpy import array
from numpy import zeros

def grid(m):

  m = int(ceil(sqrt(m)))

  print('making {:d} × {:d} grid, {:d} elements'.format(m,m,m*m))

  x = linspace(0, 1, m)
  y = linspace(0, 1, m)
  xv, yv = meshgrid(x, y)

  return column_stack((concatenate(xv), concatenate(yv)))

def circ(domain, rad=0.5):

  r = norm(array([[0.5,0.5]]) - domain, axis=1)

  return domain[r<rad,:]

def __get_inv_tesselation(tesselation):

  inv = defaultdict(set)
  for i,t in enumerate(tesselation):
    inv[t].add(i)

  return inv

def __capacity_randint(m, n):

  tesselation = zeros(m, 'int')
  tesselation_count = {k:0 for k in xrange(n)}
  cap = m/n

  for i in xrange(m):

    while True:

      r = randint(n)
      if tesselation_count[r]>cap:
        continue
      else:
        tesselation[i] = r
        tesselation_count[r] += 1
        break

  return tesselation


def point_cloud(
  domain,
  org_sites,
  tol=1.e-2,
  maxitt=10000
):

  itg = itemgetter(1)

  m = len(domain)
  n = len(org_sites)
  cap = m/n

  sites = zeros((n,2),'float')
  sites[:] = org_sites[:]

  print('point cloud')
  print('points (m): {:d}, sites (n): {:d}, cap: {:f}'.format(m,n,cap))

  tesselation = __capacity_randint(m,n) #  x → s
  inv_tesselation = __get_inv_tesselation(tesselation) # s → x

  def __get_h(dd, isi, si, sj):
    #TODO: heap. this is too slow.
    w = dd[isi,si] - dd[isi,sj]
    return dict(zip(isi, w))

  def __remap(xi,xj,si,sj):
    tesselation[xi] = sj
    tesselation[xj] = si
    inv_tesselation[si].remove(xi)
    inv_tesselation[si].add(xj)
    inv_tesselation[sj].remove(xj)
    inv_tesselation[sj].add(xi)
    return

  for k in xrange(maxitt):

    dd = cdist(domain, sites, 'euclidean')

    max_eps = -1
    i = -1
    while True:

      i += 1

      print('itt: ', k, i)

      stable = True

      for si,sj in product(xrange(n), repeat=2):

        Hi = __get_h(dd, list(inv_tesselation[si]), si, sj)
        Hj = __get_h(dd, list(inv_tesselation[sj]), sj, si)

        while Hi and Hj:

          # if Hi is heap this will be better
          xi, himax = max(Hi.iteritems(), key=itg)
          xj, hjmax = max(Hj.iteritems(), key=itg)
          eps = himax+hjmax

          max_eps = max(eps, max_eps)

          if eps<=0:
            break

          __remap(xi,xj,si,sj)
          del(Hi[xi])
          del(Hj[xj])

          stable = False

      if stable:
        break

    agg = [[] for i in repeat(None, n)]
    for t,xy in zip(tesselation, domain):
      agg[t].append(xy)

    for k, v in enumerate(agg):
      if v:
        sites[k,:] = mean(v, axis=0)

    if abs(max_eps)<tol:
      print('terminating, reached tol: {:0.5f} ({:0.5f})'.format(max_eps, tol))
      break
    else:
      print('eps {:0.5f}, going again ...'.format(max_eps))

  return sites, {k:v for k, v in inv_tesselation.iteritems() if v}

