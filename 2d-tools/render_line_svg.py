#!/usr/bin/python
# -*- coding: utf-8 -*-

BLACK = [0,0,0,1]


def make_line(c, vertices, edges, n=10):

  from numpy import arange
  from numpy import array
  from numpy.random import random
  from numpy import roll

  xys = vertices[edges]

  ii = arange(n)/float(n)

  c.new_path()

  for xy in xys:

    start = xy[0,:]
    stop = xy[1,:]
    dd = (stop-start)*random()

    c.move_to(*start)
    c.line_to(*(start+dd))

    # c.move_to(*start)
    # c.line_to(*(start+dd[::-1]*array([-1,1])))
  
  c.stroke()
  
  return

def main(args, **argv):

  from dddUtils.ioOBJ import load_2d as load
  from cairo import SVGSurface, Context
  from numpy import array
  from glob import glob

  prefix = args.prefix
  size = args.size
  scale = args.scale
  one = 1.0/size
  steps = args.steps
  stride = args.stride

  out = prefix + '.svg'
  print('making file: {:s}'.format(out))

  s = SVGSurface(out, size, size)
  c = Context(s)

  c.set_line_width(0.1)
  c.set_source_rgba(*BLACK)


  for fn in sorted(glob(prefix + '*.2obj'))[:steps:stride]:

    print(fn)

    data = load(fn)

    vertices = data['vertices']
    vertices *= scale*size
    edges = data['edges']
    make_line(c, vertices, edges)

  c.save()

  return

if __name__ == '__main__':

  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument(
    '--prefix',
    type=str,
    required=True
  )
  parser.add_argument(
    '--size',
    type=int,
    default=1000
  )
  parser.add_argument(
    '--steps',
    type=int,
    default=100000
  )
  parser.add_argument(
    '--stride',
    type=int,
    default=1
  )
  parser.add_argument(
    '--scale',
    type=float,
    default=1.0
  )

  args = parser.parse_args()

  main(args)

