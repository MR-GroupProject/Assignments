import features as ft
import json
import numpy as np
import open3d
import os
import reader

def sampler(func, folder):

    root = "LabeledDB_new"

    obj_types = reader.read_sub_fold(root)

    for obj_type in obj_types:
        
        file_paths = reader.read_file(root, obj_type, "off")
        if not os.path.exists(folder+'/'+obj_type):
            os.mkdir(folder+'/'+obj_type)
        
        for i in range(len(file_paths)):
            obj = file_paths[i]
            dic = {}
            dic["class"] = obj_type
            path_json = folder+'/'+obj_type+'/'+str(i)+".json"
            ft_list = np.zeros(20)
            mesh = open3d.io.read_triangle_mesh(obj)
            points = np.asarray(mesh.vertices)
            
            for j in range(10):
                print(obj, "round", j)
                labels, values = ft.bin(func(points, 5000), 0, 1, 20)
                ft_list += values

            dic["D2"] = (0.1*ft_list).astype("int").tolist()
            dic_json = json.dumps(dic)

            print(dic)

            file_json = open(path_json, 'w')
            file_json.write(dic_json)
            file_json.close()


sampler(ft.D2, "LabeledDB_new")