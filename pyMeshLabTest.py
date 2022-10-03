import numpy as np
import pymeshlab
import os
import polyscope as ps

import create_bbox

# Polyscope initialized
ps.init()

# create a new MeshSet
ms = pymeshlab.MeshSet()

# load a new mesh in the MeshSet, and sets it as current mesh
# the path of the mesh can be absolute or relative

ms.load_new_mesh("./LabeledDB_new/Ant/82.off")


#display the bounding box of current mesh
dim_x = ms.current_mesh().bounding_box().dim_x()
dim_y = ms.current_mesh().bounding_box().dim_y()
dim_z = ms.current_mesh().bounding_box().dim_z()
bbox_max = ms.current_mesh().bounding_box().max()
bbox_min = ms.current_mesh().bounding_box().min()
#create a off file to save the dounding box
create_bbox.creat_bounding_box_file(bbox_max, bbox_min, dim_x, dim_y, dim_z)
create_bbox.draw_bounding_box(bbox_min, bbox_max, dim_x, dim_y, dim_z)


'''
print(ms.current_mesh().face_number())
print(ms.current_mesh().vertex_number())
print(ms.current_mesh().bounding_box().dim_x())
print(ms.current_mesh().bounding_box().dim_y())
print(ms.current_mesh().bounding_box().dim_z())
print(ms.current_mesh().bounding_box().max())
print(ms.current_mesh().bounding_box().min())
print(ms.current_mesh().vertex_normal_matrix())
'''
ms.show_polyscope()

