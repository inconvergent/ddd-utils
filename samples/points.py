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



def main():

  import gtk
  from render.render import Animate
  from numpy.random import random
  from dddUtils.pointCloud import point_cloud
  from dddUtils.pointCloud import grid
  from dddUtils.pointCloud import circ

  fn = './mountain.png'

  n = 400
  m = 10000


  domain = circ(grid(m), rad=RAD)
  # domain = get_img_grid(fn)

  org_sites = (0.5-RAD) + (1.0-(0.5-RAD)*2)*random(size=(n,2))
  # org_sites = circ(org_sites, rad=RAD)

  sites, inv_tesselation = point_cloud(domain, org_sites)

  def show(render):
    render.clear_canvas()

    # grid
    render.set_front(LIGHT)
    for i, s in enumerate(domain):
      render.circle(*s, r=ONE, fill=True)

    render.set_front(BLACK)
    for s, sxy in enumerate(sites):
      render.circle(*sxy, r=ONE, fill=True)

    for s,xx in inv_tesselation.iteritems():

      sx, sy = sites[s]

      render.set_front(FRONT)
      for x in xx:
        render.line(sx, sy, domain[x,0], domain[x,1])

      render.set_front(BLACK)
      render.line(sx, sy, *org_sites[s,:])

    render.set_front(BLACK)
    for i, s in enumerate(org_sites):
      render.circle(*s, r=3*ONE, fill=True)

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

  if True:
    import pstats
    import cProfile
    OUT = 'profile'
    pfilename = '{:s}.profile'.format(OUT)
    cProfile.run('main()',pfilename)
    p = pstats.Stats(pfilename)
    p.strip_dirs().sort_stats('cumulative').print_stats()
  else:
    main()


