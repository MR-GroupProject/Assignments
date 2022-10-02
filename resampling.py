import pymeshlab as ml

ms = ml.MeshSet()
ms.load_new_mesh('./LabeledDB_new/Ant/81.off')
m = ms.current_mesh()
print('input mesh has', m.vertex_number(), 'vertex and', m.face_number(), 'faces')

# set number of points you want, it must be lower than the original number.
target = 1000

# Estimate number of faces to have 100+10000 vertex using Euler
numFaces = 100 + 2 * target

# Simplify the mesh. Only first simplification will be agressive
while ms.current_mesh().vertex_number() > target:
    ms.meshing_decimation_quadric_edge_collapse(targetfacenum=numFaces, preservenormal=True, planarquadric=True)
    print("Decimated to", numFaces, "faces mesh has", ms.current_mesh().vertex_number(), "vertex")
    # Refine our estimation to slowly converge to TARGET vertex number
    numFaces = numFaces - (ms.current_mesh().vertex_number() - target)

m = ms.current_mesh()
print('output mesh has', m.vertex_number(), 'vertex and', m.face_number(), 'faces')
ms.save_current_mesh('output.off')
ms.show_polyscope()
