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


def get_dens_from_img(fn):

  from scipy.ndimage import imread

  return 1.0-imread(fn)/255.

def get_dens_example(n):

  from dddUtils.pointCloud import grid

  x,y = grid(n,n)

  return x*y


def sample_from_dens(dens, n):

  from numpy import floor
  from numpy import zeros
  from numpy.random import random

  m = dens.shape[0]
  res = zeros((n,2),'float')
  k = 0

  while k<n:

    xy = random(2)
    ij = floor(xy*m)
    d = dens[ij[0],ij[1]]
    if random()<d:
      res[k,:] = xy
      k += 1

  return res



def main():

  import gtk
  from render.render import Animate
  from numpy.random import random
  from numpy import zeros
  from dddUtils.pointCloud import point_cloud
  from dddUtils.ioOBJ import export_2d as export
  from numpy import reshape

  fn = './mountain2.png'
  n = 300
  m = 1000

  dens = get_dens_from_img(fn)
  # dens = get_dens_example(100)

  domain = sample_from_dens(dens, m)
  org_sites = sample_from_dens(dens, n)

  sites, inv_tesselation = point_cloud(domain, org_sites, maxitt=4)

  def show(render):
    render.clear_canvas()

    render.set_front(LIGHT)
    for i, s in enumerate(domain):
      render.circle(*s, r=ONE, fill=True)

    render.set_front(BLACK)
    for s, sxy in enumerate(sites):
      render.circle(*sxy, r=3*ONE, fill=True)

    # for s,xx in inv_tesselation.iteritems():

      # sx, sy = sites[s]

      # render.set_front(FRONT)
      # for x in xx:
        # render.line(sx, sy, domain[x,0], domain[x,1])

      # render.set_front(BLACK)
      # render.line(sx, sy, *org_sites[s,:])

    # render.set_front(BLACK)
    # for i, s in enumerate(org_sites):
      # render.circle(*s, r=3*ONE, fill=False)

  def wrap(render):
    show(render)
    return False

  render = Animate(SIZE, BACK, FRONT, wrap)
  render.set_line_width(ONE)

  def __write_svg_and_exit(*args):

    gtk.main_quit(*args)
    show(render)
    render.write_to_png('./exit.png')

    export('voronoi','exit.2obj', sites)
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


