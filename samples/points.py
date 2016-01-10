#!/usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import division
from __future__ import print_function


BACK = [1,1,1,1]
FRONT = [0,0.7,0.7,0.7]
BLACK = [0,0,0,0.9]
LIGHT = [0,0,0,0.3]

SIZE = 1000
ONE = 1.0/SIZE

RAD = 0.45


def get_img_grid(fn):

  from scipy.ndimage import imread
  from numpy import row_stack
  from numpy.random import random

  domain = []

  dens = 1.0-imread(fn)/255.
  m,n = dens.shape

  rnd = random(size=m*n)

  k = 0
  for i in xrange(m):
    for j in xrange(n):
      if rnd[k]<dens[i,j]:
        domain.append([i/m,j/n])
      k += 1

  return row_stack(domain)

def get_sites(domain_dens, n):

  from numpy import floor
  from numpy import row_stack
  from numpy import zeros
  from numpy.random import random

  m = domain_dens.shape[0]

  sites = zeros((n,2),'float')
  k = 0

  while k<n:

    xy = random(2)
    ij = floor(xy*m)
    d = domain_dens[ij[0],ij[1],2]
    # print(d)
    if random()<d:
      # print(xy, ij)
      sites[k,:] = xy
      k += 1

  return row_stack(sites)



def main():

  import gtk
  from render.render import Animate
  from numpy.random import random
  from numpy import zeros
  from dddUtils.pointCloud import grid
  from dddUtils.pointCloud import point_cloud
  from numpy import reshape

  fn = './mountain.png'

  n = 200
  mx = 200
  m = mx*mx


  domain_dens = zeros((mx,mx,3), 'float')
  xv,yv = grid(mx,mx)
  domain_dens[:,:,0] = xv
  domain_dens[:,:,1] = yv
  domain_dens[:,:,2] = xv*yv

  flat = reshape(domain_dens, (m,3))
  print(flat)


  # org_sites = (0.5-RAD) + (1.0-(0.5-RAD)*2)*random(size=(n,2))
  org_sites = get_sites(domain_dens, n)
  # org_sites = circ(org_sites, rad=RAD)

  sites, inv_tesselation = point_cloud(flat, org_sites, maxitt=4)

  def show(render):
    render.clear_canvas()

    render.set_front(LIGHT)
    for i, s in enumerate(flat[:,:2]):
      render.circle(*s, r=ONE, fill=True)

    render.set_front(BLACK)
    for s, sxy in enumerate(sites):
      render.circle(*sxy, r=3*ONE, fill=True)

    for s,xx in inv_tesselation.iteritems():

      sx, sy = sites[s]

      render.set_front(FRONT)
      for x in xx:
        render.line(sx, sy, flat[x,0], flat[x,1])

      # render.set_front(BLACK)
      # render.line(sx, sy, *org_sites[s,:])

    render.set_front(BLACK)
    for i, s in enumerate(org_sites):
      render.circle(*s, r=3*ONE, fill=False)

  def wrap(render):
    show(render)
    return False

  render = Animate(SIZE, BACK, FRONT, wrap)
  render.set_line_width(ONE)

  def __write_svg_and_exit(*args):

    gtk.main_quit(*args)
    show(render)
    render.write_to_png('./exit.png')
  render.window.connect("destroy", __write_svg_and_exit)

  gtk.main()



if __name__ == '__main__':

  if False:
    import pstats
    import cProfile
    OUT = 'profile'
    pfilename = '{:s}.profile'.format(OUT)
    cProfile.run('main()',pfilename)
    p = pstats.Stats(pfilename)
    p.strip_dirs().sort_stats('cumulative').print_stats()
  else:
    main()


