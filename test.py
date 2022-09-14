from tkinter import filedialog, messagebox

from trimesh import scene
from trimesh import viewer

import tkinter
import trimesh

# scene = trimesh.Scene()
# viewer.SceneViewer(scene=scene)

def test():
    messagebox.showinfo("Test", "Hello World!")

def selectModel():
    Filepath = filedialog.askopenfilename(filetypes=[("Mesh", ("*.off", ".ply"))], initialdir=r"./")

    mesh = trimesh.load_mesh(Filepath)
    mesh.show()

window = tkinter.Tk()

window.title("Multimedia Retrieval")

window.geometry("960x540")

button_showModel = tkinter.Button(
    master=window, 
    text="Select model", 
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