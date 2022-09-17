import trimesh
import numpy as np
import pymeshlab

v = [[1, 0, 0], [1, 1, 0], [0, 1, 0], [1, 1, 1]]
f = [[0, 1, 3], [0, 1, 3], [1, 2, 3], [0, 2, 3]]
mesh = trimesh.Trimesh(vertices=v, faces=f)

# by default, Trimesh will do a light processing, which will
# remove any NaN values and merge vertices that share position
# if you want to not do this on load, you can pass `process=False`

# create a new MeshSet
ms = pymeshlab.MeshSet()

# load a new mesh in the MeshSet, and sets it as current mesh
# the path of the mesh can be absolute or relative
ms.load_new_mesh("E:/test1.ply")

print(ms.number_meshes())

# print the number of vertices of the current mesh
print(ms.current_mesh().face_number())

ms.apply_cameras_rotation(camera=1, rotcenter=1, rotaxis=1, angle=60)
ms.create_noisy_isosurface(resolution=64)

ms.show_polyscope()
