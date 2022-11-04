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
        f = len(target)
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

q = 181

all_features = dataset.get_all_data('../feature_data_modified_20bin.xlsx')

database_filepath = np.asarray(all_features)[:, -1:]
database_features = np.asarray(all_features)[:, :-1].astype(float)

a1_f = database_features[:, 0:5]
a1_rt = annoy(a1_f[q], a1_f)

first = []
for i in range(5):
    d = database_features[:, (i*20+5):(i*20+25)]
    second = annoy(d[q], d)
    first = first + list(set(second) - set(first))
    #print(first)

result = np.intersect1d(a1_rt, first)
for index in result:
    print(database_filepath[index])
#print(annoy(database_features[0], database_features))