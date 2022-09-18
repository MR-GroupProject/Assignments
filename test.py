# from tkinter import filedialog, messagebox

# from trimesh import geometry
# from trimesh import scene
# from trimesh import viewer

# from trimesh.scene import lighting

# import numpy as np
# import tkinter
# import trimesh

# mesh = trimesh.load_mesh("D:/Codes/GitHub/Assignments/LabeledDB_new/Fish/221.off")

# window_size = np.array([1280, 720])

# light = lighting.DirectionalLight(color=[255, 255, 255, 1], intensity=0, radius=1000)

# camera = scene.Camera(resolution=window_size, fov=[2.0, 2.0])

# Scene = trimesh.Scene(camera=camera, lights=[light])

# Scene.add_geometry(mesh)

# mesh.show()

from tkinter import *
from OpenGL.Tk import *

b=Opengl(height=100,width=100)
root = b.master
f = Frame(root, width=100, bg='blue')
f.pack(side='left', fill='y')
b.pack(side='right', expand=1, fill='both')

root.mainloop()