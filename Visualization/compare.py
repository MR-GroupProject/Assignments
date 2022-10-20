import numpy as np
import pymeshlab
import os
import polyscope as ps


ms = pymeshlab.MeshSet()
ps.init()
# load a new mesh in the MeshSet, and sets it as current mesh
# the path of the mesh can be absolute or relative

ms.load_new_mesh("../LabeledDB_new/Airplane/62.off")
ms.load_new_mesh("../Remesh/Airplane/62.off")
ms.set_mesh_name(newname='after normalization')

ms.show_polyscope()

