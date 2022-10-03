import numpy as np
import open3d as o3d

path = "./LabeledDB_new/Ant/82.off"

mesh = o3d.io.read_triangle_mesh(path)

#Normalization
mesh.scale(1/np.max(mesh.get_max_bound() - mesh.get_min_bound()),
           center=mesh.get_center())

o3d.visualization.draw_geometries([mesh])

#Voxelization
voxel_grid = o3d.geometry.VoxelGrid.create_from_triangle_mesh(mesh,
                                                              voxel_size=0.05)
o3d.visualization.draw_geometries([voxel_grid])