from tkinter import filedialog

import tkinter as tk
import trimesh


root = tk.Tk()
root.withdraw()

Filepath = filedialog.askopenfilename(filetypes=[("Mesh", ("*.off", ".ply"))], initialdir=r"./")

mesh = trimesh.load_mesh(Filepath)

mesh.show()