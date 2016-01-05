#!/usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import print_function

from dddUtils.random import naive_lloyd
from render.render import Animate

BACK = [1,1,1,1]
FRONT = [0,0.5,0.5,0.7]
SIZE = 520
ONE = 1.0/SIZE

ALPHA = 0.5
MAXITT = 1000
MS = 5


def grid(n):

  from numpy import linspace
  from numpy import meshgrid
  from numpy import column_stack
  from numpy import concatenate

  x = linspace(0, 1, n)
  y = linspace(0, 1, n)
  xv, yv = meshgrid(x, y)
  return column_stack((concatenate(xv), concatenate(yv)))

def circ(domain, lim=0.5):

  from numpy.linalg import norm
  from numpy import array
  r = norm(array([[0.5,0.5]]) - domain, axis=1)
  mask = r<lim
  print(mask)
  return domain[mask,:]


def main():

  import gtk
  from render.render import Animate
  from numpy.random import random
  from numpy import array

  domain = circ(grid(200))
  sites = random(size=(2000,2))

  nl = naive_lloyd(domain, sites, max_itt=MAXITT)

  def wrap(render):

    sites = nl.next()
    render.set_front(FRONT)
    render.clear_canvas()
    for i, s in enumerate(sites):
      render.circle(*s, r=2*ONE, fill=True)

    fn = './asdf_{:05d}.png'
    render.write_to_png(fn.format(render.num_img))
    print(fn)

    return True

  render = Animate(SIZE, BACK, FRONT, wrap)
  render.set_line_width(ONE)


  gtk.main()



if __name__ == '__main__':

  main()

