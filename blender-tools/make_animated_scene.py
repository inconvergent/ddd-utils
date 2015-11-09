# -*- coding: utf-8 -*-

import bpy


def main(argv):

  from glob import glob
  from dddUtils.blender import Obj

  prefix = argv[0]
  fn_out = argv[1]

  objs = []
  count = 0

  for fn in sorted(glob('{:s}*.obj'.format(prefix))):

    print('importing: ' + fn)

    O = Obj(fn, 'a')
    O.set_smooth_shade()
    O.move_rescale(set_pivot=[0.5,-0.5,0.5], pos=[0,0,0], scale=100)
    O.smooth()
    O.animate_vis(count, count+1)
    O.apply_mat()
    objs.append(O)

    count += 1

  bpy.data.scenes['Scene'].frame_current = 1
  bpy.data.scenes['Scene'].frame_end = count-1

  bpy.ops.wm.save_as_mainfile(filepath=fn_out)


if __name__ == '__main__':

  import sys
  argv = sys.argv
  argv = argv[argv.index("--") + 1:]
  main(argv)

