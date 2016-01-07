# -*- coding: utf-8 -*-


from __future__ import division
from __future__ import print_function


def export_svg(fn, paths, size, line_with=0.1, scale_factor=None):

  from cairo import SVGSurface, Context
  from numpy import array
  from ddd import spatial_sort_2d as sort

  if not scale_factor:
    scale_factor = size

  one = 1.0/size
  s = SVGSurface(fn, size, size)
  c = Context(s)

  c.set_line_width(0.1)

  paths = sort(paths)

  for path in paths:
    path *= scale_factor

    c.new_path()
    c.move_to(*path[0,:])
    for p in path[1:]:
      c.line_to(*p)
    c.stroke()

  c.save()

