import pymeshlab
import polyscope as ps
from visualization import create_bbox

# Polyscope initialized
ps.init()

# create a new MeshSet
ms = pymeshlab.MeshSet()

# load a new mesh in the MeshSet, and sets it as current mesh
# the path of the mesh can be absolute or relative

ms.load_new_mesh("../LabeledDB_new/Airplane/72.off")


# display the bounding box of current mesh
dim_x = ms.current_mesh().bounding_box().dim_x()
dim_y = ms.current_mesh().bounding_box().dim_y()
dim_z = ms.current_mesh().bounding_box().dim_z()
bbox_max = ms.current_mesh().bounding_box().max()
bbox_min = ms.current_mesh().bounding_box().min()

mesh_face_matrix = ms.current_mesh().face_matrix()
mt = ms.current_mesh().vertex_matrix()
# create a off file to save the bounding box
create_bbox.creat_bounding_box_file(bbox_max, bbox_min, dim_x, dim_y, dim_z)
create_bbox.draw_bounding_box(bbox_min, bbox_max, dim_x, dim_y, dim_z)

ms.show_polyscope()

