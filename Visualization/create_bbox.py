import numpy as np
import pymeshlab
import os
import polyscope as ps

def creat_bounding_box_file(bbox_max, bbox_min, dim_x, dim_y, dim_z):

    f = open('../bounding_box.off', 'w')
    f.write('OFF\n')
    f.write('8 6 0\n')
    # 4 lower vertexs
    f.write(str(bbox_min[0]) + ' '+ str(bbox_min[1]) + ' ' + str(bbox_min[2]) + '\n')                    #0 000 xmin, ymin, zmin
    f.write(str(bbox_min[0] + dim_x) + ' '+ str(bbox_min[1]) + ' ' + str(bbox_min[2]) + '\n')            #1 100 xmin + dimx, ymin, zmin
    f.write(str(bbox_min[0]+ dim_x) + ' '+ str(bbox_min[1] + dim_y) + ' ' + str(bbox_min[2]) + '\n')     #2 110 xmin, ymin + dimy, zmin
    f.write(str(bbox_min[0]) + ' '+ str(bbox_min[1] + dim_y) + ' ' + str(bbox_min[2]) + '\n')            #3 010 xmin = dimx, ymin + dimy, zmin

    # 4 upper vertexs
    f.write(str(bbox_max[0]) + ' '+ str(bbox_max[1]) + ' ' + str(bbox_max[2]) + '\n')                    #4 111 xmax, ymax, zmax
    f.write(str(bbox_max[0] - dim_x) + ' '+ str(bbox_max[1]) + ' ' + str(bbox_max[2]) + '\n')            #5 011 xmax - dimx, ymax, zmax
    f.write(str(bbox_max[0]- dim_x) + ' '+ str(bbox_max[1] - dim_y) + ' ' + str(bbox_max[2]) + '\n')     #6 001 xmax, ymax - dimy, zmax
    f.write(str(bbox_max[0]) + ' '+ str(bbox_max[1] - dim_y) + ' ' + str(bbox_max[2]) + '\n')            #7 101 xmax - dimx, ymax - dimy, zmax
    
    #faces
    f.write('4 0 1 2 3\n') 
    f.write('4 4 5 6 7\n') 
    f.write('4 2 3 5 4\n') 
    f.write('4 0 1 7 6\n') 
    f.write('4 1 2 4 7\n') 
    f.write('4 0 3 5 6\n') 
    f.close()
    return

def draw_bounding_box(bbox_min, bbox_max, dim_x, dim_y, dim_z):
#draw a bounding box by polyscope.
    bx_vertex = np.array([
        [bbox_min[0], bbox_min[1], bbox_min[2]],
        [bbox_min[0] + dim_x, bbox_min[1], bbox_min[2]],
        [bbox_min[0] + dim_x, bbox_min[1] + dim_y, bbox_min[2]],
        [bbox_min[0], bbox_min[1] + dim_y, bbox_min[2]],
        [bbox_max[0], bbox_max[1], bbox_max[2]],
        [bbox_max[0] - dim_x, bbox_max[1], bbox_max[2]],
        [bbox_max[0]- dim_x, bbox_max[1] - dim_y, bbox_max[2]],
        [bbox_max[0], bbox_max[1] - dim_y, bbox_max[2]]
    ])
    bx_face = np.array([
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [2, 3, 5, 4],
        [0, 1, 7, 6],
        [1, 2, 4, 7],
        [0, 3, 5, 6]
    ])

    polyscope_bounding_box = ps.register_surface_mesh('bx', bx_vertex, bx_face)
    polyscope_bounding_box.set_transparency(0.5)
    polyscope_bounding_box.set_edge_width(4)
    polyscope_bounding_box.set_color([255, 255, 255])