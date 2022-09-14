from tkinter import filedialog

import tkinter as tk
import trimesh


root = tk.Tk()
root.withdraw()

Filepath = filedialog.askopenfilename(initialdir=r"LaberledDB_new")

mesh = trimesh.load_mesh(Filepath)

mesh.show()