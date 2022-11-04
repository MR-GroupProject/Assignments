from annoy import AnnoyIndex
import random
from tools import dataset
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import path

def annoy (target, database):
    if type(target) == int or type(target) == float:

        return
    else:
        f = 105
        t = AnnoyIndex(f, 'manhattan')  # Length of item vector that will be indexed
        i = 0
        for data in database:
            t.add_item(i, data)
            i +=1

        t.build(19) # 10 trees
        t.save('test.ann')

        u = AnnoyIndex(f, 'manhattan')
        u.load('test.ann') # super fast, will just mmap the file
        a = u.get_nns_by_vector(target, 50) # will find the 1000 nearest neighbors
        return a 



# read feature
all_features = dataset.get_all_data('../feature_data_modified_20bin.xlsx')

database_filepath = np.asarray(all_features)[:, -1:]
database_features = np.asarray(all_features)[:, :-1].astype(float)
print(annoy(database_features[0], database_features))