import bpy


def main(argv):

  from time import time
  from dddUtils.blender import Cloud

  fn = argv[0]
  img_out = argv[1]

  try:
    scale = argv[2]
  except Exception:
    scale = 1.0

  print('importing: ' + fn)

  t1 = time()

  C = Cloud(fn,'a')
  C.move_rescale(set_pivot=[0.5,-0.5,0.5], pos=[0,0,0], scale=scale)
  C.spheres(scale=0.0005)

  print('\ntime:',time()-t1,'\n\n')

  bpy.data.scenes["Scene"].render.filepath = img_out
  bpy.ops.render.render(write_still=True)


if __name__ == '__main__':

  import sys
  argv = sys.argv

  argv = argv[argv.index("--") + 1:]
  main(argv)

