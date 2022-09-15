from tkinter import filedialog, messagebox

from trimesh import geometry
from trimesh import scene
from trimesh import viewer

from trimesh.scene import lighting

import numpy as np
import tkinter
import trimesh

window_size = np.array([1280, 720])

light = lighting.DirectionalLight(color=[255, 255, 255, 1], intensity=0, radius=1000)

camera = scene.Camera(resolution=window_size, fov=[2.0, 2.0])

Scene = trimesh.Scene()

def test():
    messagebox.showinfo("Test", "Hello World!")

def selectModel():
    filePaths = filedialog.askopenfilenames(filetypes=[("Mesh", ("*.off", ".ply"))], initialdir=r"./")

    selectedNumber = len(filePaths)

    if selectedNumber == 0:
        return

    for i in range(selectedNumber):
        mesh = trimesh.load_mesh(filePaths[i])
        mesh.apply_translation([i-selectedNumber/2, 0, 0])
        Scene.add_geometry(mesh)

    Scene.show()
    

window = tkinter.Tk()

window.title("Multimedia Retrieval")

window.geometry("960x540")

button_showModel = tkinter.Button(
    master=window, 
    text="Select models", 
    command=selectModel, 
    height=2, 
    width=15)

button_showModel.grid(column=0, row=0, padx=10, pady=10)

button_test = tkinter.Button(
    master=window, 
    text="Test", 
    command=test, 
    height=2, 
    width=15)

button_test.grid(column=0, row=1, padx=10, pady=10)

window.mainloop()