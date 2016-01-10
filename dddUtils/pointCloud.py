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
from numpy import square
from numpy import linspace
from numpy import meshgrid
from numpy import column_stack
from numpy import row_stack
from numpy import zeros
from numpy import array
from numpy import reshape


def grid(m, n):

  print('making {:d} × {:d} grid, {:d} elements'.format(m,n,m*n))

  x = linspace(0, 1, m)
  y = linspace(0, 1, n)
  return meshgrid(x, y)

def __get_inv_tesselation(tesselation):

  inv = defaultdict(set)
  for i,t in enumerate(tesselation):
    inv[t].add(i)

  # print([len(i) for i in inv.values()])

  return inv

def __capacity_randint(m, n):

  tesselation = zeros(m, 'int')
  tesselation_count = {k:0 for k in xrange(n)}
  cap = m/n

  for i in xrange(m):

    while True:

      r = randint(n)
      if tesselation_count[r]>=cap:
        continue
      else:
        tesselation[i] = r
        tesselation_count[r] += 1
        break

  return tesselation


def point_cloud(
  flat,
  org_sites,
  tol=1.e-2,
  maxitt=10000
):

  itg = itemgetter(1)

  m = len(flat)
  n = len(org_sites)
  cap = m/n

  sites = zeros((n,2),'float')
  sites[:] = org_sites[:]

  print('point cloud')
  print('points (m): {:d}, sites (n): {:d}, cap: {:f}'.format(m,n,cap))


  def __get_h(dd, isi, si, sj):
    #TODO: heap. this is too slow.
    w = dd[isi,si] - dd[isi,sj]
    return dict(zip(isi, w))

  def __remap(tes, inv, xi,xj,si,sj):
    tes[xi] = sj
    tes[xj] = si
    inv[si].remove(xi)
    inv[si].add(xj)
    inv[sj].remove(xj)
    inv[sj].add(xi)
    return

  for k in xrange(maxitt):

    dd = cdist(flat[:,:2], sites, 'euclidean')
    tesselation = __capacity_randint(m,n) #  x → s
    inv_tesselation = __get_inv_tesselation(tesselation) # s → x

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

          __remap(tesselation, inv_tesselation, xi,xj,si,sj)
          del(Hi[xi])
          del(Hj[xj])

          stable = False

      if stable:
        break

    agg = [[] for i in repeat(None, n)]
    for t,xyp in zip(tesselation, flat):
      agg[t].append(xyp)

    for k, v in enumerate(agg):
      if v:
        v = row_stack(v)

        tot = v[:,2].sum()
        sa = (v[:,:2]*v[:,2:]).sum(axis=0)/tot


        sb = mean(v[:,:2], axis=0)
        sites[k,:] = sb

        print(sa,sb,norm(sa-sb))

    cap_count = array([len(v) for v in inv_tesselation.values()],'float')
    cap_err = square(cap_count/float(cap)-1.0).sum()/n

    if abs(max_eps)<tol:
      pr('terminating, reached tol: {:0.5f} ({:0.5f})'.format(max_eps, tol))
      print('capacity error: {:0.5f}'.format(cap_err))
      break
    else:
      print('eps {:0.5f}, going again ...'.format(max_eps))
      print('capacity error: {:0.5f}'.format(cap_err))

  return sites, {k:v for k, v in inv_tesselation.iteritems() if v}

