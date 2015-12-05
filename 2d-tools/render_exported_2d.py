#!/usr/bin/python
# -*- coding: utf-8 -*-


def get_mid(v):

  from numpy import array

  mi = v.min(axis=0).squeeze()
  ma = v.max(axis=0).squeeze()
  midx = (mi[0]+ma[0])*0.5
  midy = (mi[1]+ma[1])*0.5
  move = array([[midx,midy]])
  return move

def main(args):

  from render.render import Render
  from dddUtils.ioOBJ import load
  from numpy import array

  data = load(args.fn)

  size = args.size
  one = 1.0/size
  vertices = data['vertices'][:,:2]

  back = [1,1,1,1]
  front = [0,0,0,args.alpha]

  rad = args.rad*one

  vertices -= get_mid(vertices)
  vertices *= args.scale
  vertices += array([[0.5,0.5]])

  render = Render(size, back, front)

  render.ctx.set_source_rgba(*front)
  render.ctx.set_line_width(one)

  out = ''.join(args.fn.split('.')[:-1])+'.png'

  for vv in vertices:
    render.circle(vv[0], vv[1], rad, fill=True)

  render.write_to_png(out)

  return

if __name__ == '__main__':

  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument(
    '--fn',
    type=str,
    required=True
  )
  parser.add_argument(
    '--rad',
    type=float,
    default=1
  )
  parser.add_argument(
    '--size',
    type=int,
    default=2048
  )
  parser.add_argument(
    '--alpha',
    type=float,
    default=0.1
  )
  parser.add_argument(
    '--scale',
    type=float,
    default=1.0
  )

  args = parser.parse_args()

  main(args)

