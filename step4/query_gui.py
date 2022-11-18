import os
import trimesh
import polyscope as ps
import tkinter as tk
from tkinter import filedialog
from matching import Matching


root = '../Remesh'
result_meshes = []
debug_mesh = []
match = []
labels = []
ps.init()


def selectModel():
    match.clear()
    result_meshes.clear()
    for label in labels:
        label.destroy()
    label_loading.grid()
    filePath = filedialog.askopenfilename(filetypes=[("Mesh", ("*.off", ".ply"))], initialdir=root)
    if filePath != '' and filePath is not None:
        filename = os.path.basename(filePath)
        classname = os.path.dirname(filePath)
        query_path = root + '/' + os.path.basename(classname) + '/' + filename
        m = Matching(query_path)
        match.append(m)
        matches, classes, descriptors, distances = m.match()

        q_mesh = trimesh.load_mesh(filePath)
        ps.register_surface_mesh("query mesh", q_mesh.vertices, q_mesh.faces)

        head = [('Query mesh: ' + filename), 'A3', 'D1', 'D2', 'D3', 'D4', 'Distance']
        for col in range(1, 8):
            if col < 3:
                l_head = tk.Label(window, text=head[col - 1], font=('Arial', 10), width=20, height=2)
            else:
                l_head = tk.Label(window, text=head[col - 1], font=('Arial', 10), width=10, height=2)
            l_head.grid(column=col, row=0, padx=10, pady=10)
            labels.append(l_head)

        for i in range(1, 11):
            match_file = os.path.basename(matches[i - 1])
            match_class = os.path.basename(os.path.dirname(matches[i - 1]))
            label = tk.Label(window, text=str(match_class + '/' + match_file), bg='grey', font=('Arial', 10), width=20, 
                             height=2)
            label.grid(column=1, row=i, padx=10, pady=10)
            labels.append(label)

            for j in range(2, 7):
                l_dist = tk.Label(window, text=str(round(descriptors[i - 1][j - 2], 3)), font=('Arial', 10), width=5,
                                  height=2)
                l_dist.grid(column=j, row=i, padx=10, pady=10)
                labels.append(l_dist)

            l_final_d = tk.Label(window, text=str(round(distances[i - 1], 3)), font=('Arial', 10), width=10, height=2)
            l_final_d.grid(column=7, row=i, padx=10, pady=10)
            labels.append(l_final_d)

            mesh = trimesh.load_mesh(matches[i - 1])
            result_meshes.append(mesh)

            button_view_each = tk.Button(
                master=window,
                text="View",
                height=2,
                width=10)
            button_view_each.bind("<Button-1>", get_button)
            button_view_each.grid(column=8, row=i, padx=10, pady=10)
            labels.append(button_view_each)

    button_debug = tk.Button(
        master=window,
        text="Debug",
        command=debug,
        height=2,
        width=15)

    button_debug.grid(column=0, row=2, padx=10, pady=10)
    labels.append(button_debug)
    button_ann = tk.Button(
        master=window,
        text="ANN",
        command=ann,
        height=2,
        width=15)

    button_ann.grid(column=0, row=1, padx=10, pady=10)
    labels.append(button_ann)
    label_loading.grid_remove()


def get_button(event):
    button_row = event.widget.grid_info().get('row')
    show(result_meshes[button_row-1])


def get_debug(event):
    show(debug_mesh[0])


def show(mesh, enable=0):
    if enable == 0:
        ps.get_surface_mesh('query mesh').set_enabled(False)
        ps.register_surface_mesh("result mesh", mesh.vertices, mesh.faces)
        ps.get_surface_mesh('result mesh').set_position([1.2, 0, 0])
    else:
        ps.get_surface_mesh('query mesh').set_enabled(True)
        print(ps.get_surface_mesh('result mesh'))
    ps.show()


def debug():
    debug_mesh.clear()
    filePath = filedialog.askopenfilename(filetypes=[("Mesh", ("*.off", ".ply"))], initialdir=root)
    m = match[0]
    descriptors = []
    if filePath != '' and filePath is not None:

        filename = os.path.basename(filePath)
        classname = os.path.dirname(filePath)
        debug_path = root + '/' + os.path.basename(classname) + '/' + filename
        # chosen_f = np.asarray(m.get_feature_by_path(debug_path)).reshape(1, -1)
        # chosen_const_f = m.get_q_const_f(debug_path).reshape(1, -1)

        # const = m.get_const_distance(chosen_const_f)
        # a3, d1, d2, d3, d4 = m.get_hist_distance(chosen_f)
        # descriptors.extend(a3)
        # descriptors.extend(d1)
        # descriptors.extend(d2)
        # descriptors.extend(d3)
        # descriptors.extend(d4)
        # descriptors.append(np.mean([const[0], const[1], const[2], const[3], const[4], const[5], a3, d1, d2, d3, d4]))
        for i in range(len(m.data_filepath)):
            if m.data_filepath[i][0] == debug_path:
                descriptors = m.descriptors_results.get(i)
                descriptors.append(m.distance_results.get(i))
                break

        label = tk.Label(window, text=str('debug:' + os.path.basename(classname) + '/' + filename), bg='grey',
                         font=('Arial', 10), width=20, height=2)
        label.grid(column=1, row=11, padx=10, pady=10)
        labels.append(label)

        for col in range(2, 8):
            l_dist = tk.Label(window, text=str(round(descriptors[col-2], 3)), font=('Arial', 10), width=10, height=2)
            l_dist.grid(column=col, row=11, padx=10, pady=10)
            labels.append(l_dist)

        mesh = trimesh.load_mesh(debug_path)
        debug_mesh.append(mesh)

        button_view_each = tk.Button(
            master=window,
            text="View",
            height=2,
            width=10)
        button_view_each.bind("<Button-1>", get_debug)
        button_view_each.grid(column=8, row=11, padx=10, pady=10)
        labels.append(button_view_each)


def ann():
    m = match[0]
    matches = m.match_by_annoy()
    l_head = tk.Label(window, text='ANN results', font=('Arial', 10), width=10, height=2)
    l_head.grid(column=10, row=0, padx=10, pady=10)
    labels.append(l_head)
    for i in range(1, 11):
        match_file = os.path.basename(matches[i - 1])
        match_class = os.path.basename(os.path.dirname(matches[i - 1]))
        label = tk.Label(window, text=str(match_class + '/' + match_file), bg='grey', font=('Arial', 10), width=20,
                         height=2)
        label.grid(column=10, row=i, padx=10, pady=10)
        labels.append(label)


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

button_showModel.grid(column=0, row=0, padx=10, pady=10)

window.mainloop()

