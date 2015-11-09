# 3D Utils

This library is a collection of useful functions I find myself re-implementing
across repositories when working with 3d meshes in general and Blender in
particular.

## Note

The layout is like this:

```
    └── dddUtils
        ├── blender.py
        ├── ddd.py
        ├── __init__.py
        └── ioOBJ.py
```

`blender.py` should only be used inside scripts called within the context of
Blender.

The remaining code should hopefully be compatible with both Python2 and Python3,
so it can be installed and imported in either environment.

## Used in

*    https://github.com/inconvergent/differential-cloud
*    https://github.com/inconvergent/differential-mesh-3d
*    https://github.com/inconvergent/differential-line-mpi



-----------
http://inconvergent.net

