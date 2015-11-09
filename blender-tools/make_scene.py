# -*- coding: utf-8 -*-

import bpy


def main(argv):

  from dddUtils.blender import Obj

  name = argv[0]
  fn_out = argv[1]

  print('importing: ' + name)

  O = Obj(name, 'a')
  O.smooth()
  O.set_smooth_shade()
  O.move_rescale(set_pivot=[0.5,-0.5,0.5], pos=[0,0,0], scale=100)
  O.apply_mat()

  bpy.ops.wm.save_as_mainfile(filepath=fn_out)


if __name__ == '__main__':

  import sys
  argv = sys.argv
  argv = argv[argv.index("--") + 1:]
  main(argv)

