import trimesh
import numpy as np
import pymeshlab

# create a new MeshSet
ms = pymeshlab.MeshSet()

# load a new mesh in the MeshSet, and sets it as current mesh
# the path of the mesh can be absolute or relative

ms.load_new_mesh("./PLY/ant.ply")

# print(ms.number_meshes())

# print the number of vertices and faces of the current mesh
print(ms.current_mesh().face_number())
print(ms.current_mesh().vertex_number())

ms.show_polyscope()
