import os


def read_sub_fold(root="../Remesh"):
    return os.listdir(root)


def read_file(folder, root="../Remesh"):
    d = os.path.join(root, folder)
    path_list = []
    for file in os.listdir(d):
        off_path = root + '/' + folder + '/' + file
        path_list.append(off_path)
    return path_list

