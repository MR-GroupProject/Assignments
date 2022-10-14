import json
import numpy as np
import open3d
import os

# file_path = open("file_path.txt", 'w')
# file_path_json = open("file_path_json.txt", 'w')

def read_subfold():
    return os.listdir("LabeledDB_new")

def read_file(folder):
    d = os.path.join("LabeledDB_new", folder)
    path_list = []
    for file in os.listdir(d):
        if file.endswith('.off'):
            off_path = "LabeledDB_new/"+folder+'/'+file
            path_list.append(off_path)
    return path_list

            
        # if not os.path.exists("npy"+'/'+sub_fold):
        #     os.mkdir("npy"+'/'+sub_fold)
        # if not os.path.exists("json"+'/'+sub_fold):
        #     os.mkdir("json"+'/'+sub_fold)
        #         mesh = open3d.io.read_triangle_mesh(off_path)

        #         vertices = np.asarray(mesh.vertices)
        #         triangles = np.asarray(mesh.triangles)
                
        #         # Save json file

        #         dic = {}
        #         dic["vertices"] = vertices.tolist()
        #         dic["triangles"] = triangles.tolist()
        #         dic_json = json.dumps(dic)
        #         file_json = open(path_json, 'w')
        #         file_json.write(dic_json)
        #         file_json.close()

        #         # Save npy file

        #         npy_path = "npy"+'/'+sub_fold+'/'+file.split('.')[0]+'_'
        #         np.save(npy_path+"vertices.npy", vertices)
        #         np.save(npy_path+"triangles.npy", triangles)            

        #         path_json_list.append(int(file.split('.')[0]))
        # path_json_list.sort()
        # for aaa in path_json_list:
        #     path_json = "json"+'/'+sub_fold+'/'+str(aaa)+'.json\n'
        #     file_path_json.write(path_json)