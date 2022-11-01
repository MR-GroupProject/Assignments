import os
from tkinter import filedialog, messagebox

import trimesh
import polyscope as ps
from trimesh import viewer

import numpy as np
import tkinter as tk
import pymeshlab

from Step4 import matching


root = '../Remesh'
result_meshes = []
labels = []
ps.init()


def selectModel():
    result_meshes.clear()
    for label in labels:
        label.destroy()
    label_loading.grid()
    filePath = filedialog.askopenfilename(filetypes=[("Mesh", ("*.off", ".ply"))], initialdir=root)
    if filePath != '' and filePath is not None:
        filename = os.path.basename(filePath)
        classname = os.path.dirname(filePath)
        query_path = root + '/' + os.path.basename(classname) + '/' + filename

        matches, classes, descriptors, distances = matching.match(query_path)
        q_mesh = trimesh.load_mesh(filePath)
        ps.register_surface_mesh("query mesh", q_mesh.vertices, q_mesh.faces)
        head = [('Query mesh: ' + filename), 'Single-value descriptors', 'A3', 'D1', 'D2', 'D3', 'D4', 'Distance']
        for col in range(1, 9):
            if col < 3:
                l_head = tk.Label(window, text=head[col - 1], font=('Arial', 10), width=20, height=2)
            else:
                l_head = tk.Label(window, text=head[col - 1], font=('Arial', 10), width=10, height=2)
            l_head.grid(column=col, row=0, padx=10, pady=10)
            labels.append(l_head)

        for i in range(1, 11):
            label = tk.Label(window, text=matches[i - 1], bg='grey', font=('Arial', 10), width=25, height=2)
            label.grid(column=1, row=i, padx=10, pady=10)
            l_dist = tk.Label(window, text=str(round(descriptors[i - 1][0], 3)), font=('Arial', 10), width=20, height=2)
            l_dist.grid(column=2, row=i, padx=10, pady=10)
            l_a3 = tk.Label(window, text=str(round(descriptors[i - 1][1], 3)), font=('Arial', 10), width=10, height=2)
            l_a3.grid(column=3, row=i, padx=10, pady=10)
            l_d1 = tk.Label(window, text=str(round(descriptors[i - 1][2], 3)), font=('Arial', 10), width=10, height=2)
            l_d1.grid(column=4, row=i, padx=10, pady=10)
            l_d2 = tk.Label(window, text=str(round(descriptors[i - 1][3], 3)), font=('Arial', 10), width=10, height=2)
            l_d2.grid(column=5, row=i, padx=10, pady=10)
            l_d3 = tk.Label(window, text=str(round(descriptors[i - 1][4], 3)), font=('Arial', 10), width=10, height=2)
            l_d3.grid(column=6, row=i, padx=10, pady=10)
            l_d4 = tk.Label(window, text=str(round(descriptors[i - 1][5], 3)), font=('Arial', 10), width=10, height=2)
            l_d4.grid(column=7, row=i, padx=10, pady=10)

            l_final_d = tk.Label(window, text=str(round(distances[i - 1], 3)), font=('Arial', 10), width=10, height=2)
            l_final_d.grid(column=8, row=i, padx=10, pady=10)

            mesh = trimesh.load_mesh(matches[i - 1])
            result_meshes.append(mesh)

            button_view_each = tk.Button(
                master=window,
                text="View",
                height=2,
                width=15)
            button_view_each.bind("<Button-1>", get_button)
            button_view_each.grid(column=9, row=i, padx=10, pady=10)
            labels.append(button_view_each)
            labels.append(label)
            labels.append(l_dist)
            labels.append(l_a3)
            labels.append(l_d1)
            labels.append(l_d2)
            labels.append(l_d3)
            labels.append(l_d4)
            labels.append(l_final_d)

        button_view = tk.Button(
            master=window,
            text="View",
            command=lambda: show(q_mesh, enable=1),
            height=2,
            width=15)

        button_view.grid(column=0, row=0, padx=10, pady=10)
        labels.append(button_view)

    label_loading.grid_remove()
    #  ms.show_polyscope()


def get_button(event):
    button_row = event.widget.grid_info().get('row')
    show(result_meshes[button_row-1])


def show(mesh, enable=0):
    if enable == 0:
        ps.get_surface_mesh('query mesh').set_enabled(False)
        ps.register_surface_mesh("result mesh", mesh.vertices, mesh.faces)
        ps.get_surface_mesh('result mesh').set_position([1.2, 0, 0])
    ps.show()


window = tk.Tk()
window.title("Multimedia Retrieval")

window.geometry("1920x1080")
label_loading = tk.Label(window, text='querying...', font=('Arial', 10), width=20, height=2)
label_loading.grid(column=5, row=1, padx=50, pady=10)
label_loading.grid_remove()

button_showModel = tk.Button(
    master=window,
    text="Select models",
    command=selectModel,
    height=2,
    width=15)

button_showModel.grid(column=0, row=1, padx=10, pady=10)

window.mainloop()

'''for i in range(10):
    ms.load_new_mesh(matches[i])
    label = tk.Label(window, text=matches[i], bg='grey', font=('Arial', 10), width=20, height=2)
    label.grid(column=1, row=i, padx=10, pady=10)
    button_view = tk.Button(
        master=window,
        text="View",
        command=show,
        height=2,
        width=15)

    button_view.grid(column=3, row=i, padx=10, pady=10)'''
