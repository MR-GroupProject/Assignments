import features as ft
from tools import dataset
from tools import reader


def get_all_features():
    features = []

    obj_types = reader.read_sub_fold()
    for obj_type in obj_types:
        print(obj_type)
        file_paths = reader.read_file(obj_type)
        for obj in file_paths:
            one_mesh_features = ft.get_feature(obj)
            one_mesh_features.append(str(obj))
            features.append(one_mesh_features)
            print(obj)

    return features


wb, ws = dataset.create_table('../data/feature_data_modified_20bin.xlsx')
descriptors = get_all_features()
dataset.write_data(descriptors, ws)
wb.close()
