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
  sites,
  eps=1.e-3
):

  itg = itemgetter(1)

  m = len(domain)
  n = len(sites)
  cap = m/n

  print('point cloud')
  print('points (m): {:d}, sites (n): {:d}, cap: {:f}'.format(m,n,cap))

  tesselation = __capacity_randint(m,n) #  x → s
  inv_tesselation = __get_inv_tesselation(tesselation) # s → x

  print(tesselation)

  i = 0
  while True:

    i += 1

    print('itt: ', i)

    stable = True

    for si,sj in product(xrange(n), repeat=2):

      # do dst calcs elsewhere?
      # Hi should be heap or otherwise sorted, to easily retieve max

      sixy = sites[si,:]
      sjxy = sites[sj,:]
      isi = list(inv_tesselation[si])
      isj = list(inv_tesselation[sj])

      isidst = norm(domain[isi,:]-sixy, axis=1) - norm(domain[isi,:]-sjxy, axis=1)
      isjdst = norm(domain[isj,:]-sjxy, axis=1) - norm(domain[isj,:]-sixy, axis=1)
      Hi = {x:d for x,d in zip(isi, isidst)}
      Hj = {x:d for x,d in zip(isj, isjdst)}

      while Hi and Hj:

        # if Hi is heap this will be better
        xi, himax = max(Hi.iteritems(), key=itg)
        xj, hjmax = max(Hj.iteritems(), key=itg)

        eps = himax+hjmax

        if eps<=0:
          break

        stable = False

        tesselation[xi] = sj
        tesselation[xj] = si

        inv_tesselation[si].remove(xi)
        inv_tesselation[si].add(xj)

        inv_tesselation[sj].remove(xj)
        inv_tesselation[sj].add(xi)

        del(Hi[xi])
        del(Hj[xj])


    if stable:
      break

  agg = [[] for i in repeat(None, n)]
  for t,xy in zip(tesselation, domain):
    agg[t].append(xy)

  sites = {k:mean(v, axis=0) for k,v in enumerate(agg) if v}

  return sites, {k:v for k, v in inv_tesselation.iteritems() if v}
