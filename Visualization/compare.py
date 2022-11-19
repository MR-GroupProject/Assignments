import pymeshlab
import polyscope as ps


ms = pymeshlab.MeshSet()
ps.init()

ms.load_new_mesh("../Remesh/Airplane/62.off")
ms.load_new_mesh("../Remesh/Airplane/62.off")
ms.set_mesh_name(newname='after normalization')

ms.show_polyscope()

