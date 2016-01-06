# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function


def export_svg(fn, paths, size):

  from cairo import SVGSurface, Context
  from numpy import array

  one = 1.0/size
  s = SVGSurface(fn, size, size)
  c = Context(s)

  c.set_line_width(0.1)

  paths = spatial_sort(paths)

  for path in paths: 
    path *= size

    c.new_path()
    c.move_to(*path[0,:])
    for p in path[1:]:
      c.line_to(*p)
    c.stroke()

