import trimesh
import numpy as np
import pymeshlab

# create a new MeshSet
ms = pymeshlab.MeshSet()

# load a new mesh in the MeshSet, and sets it as current mesh
# the path of the mesh can be absolute or relative

ms.load_new_mesh("./LabeledDB_new/Ant/81.off")

# print(ms.number_meshes())

# print the number of vertices and faces of the current mesh
print(ms.current_mesh().face_number())
print(ms.current_mesh().vertex_number())
print(ms.current_mesh().bounding_box().dim_x())
print(ms.current_mesh().bounding_box().dim_y())
print(ms.current_mesh().bounding_box().dim_z())
print(ms.current_mesh().bounding_box().max())
print(ms.current_mesh().bounding_box().min())
print(ms.current_mesh().vertex_normal_matrix())

#ms.show_polyscope()
