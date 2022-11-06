from annoy import AnnoyIndex
import random
from tools import dataset
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import path





def annoy(target, database):
    if type(target) == int or type(target) == float:

        return
    else:
        f = len(target)
        t = AnnoyIndex(f, 'euclidean')  # 'euclidean' Length of item vector that will be indexed
        i = 0
        for data in database:
            t.add_item(i, data)
            i +=1

        t.build(19) # 10 trees
        t.save('test.ann')

        u = AnnoyIndex(f, 'euclidean')
        u.load('test.ann') # super fast, will just mmap the file
        a = u.get_nns_by_vector(target, 20) # will find the 1000 nearest neighbors
        return a 



# read feature

q = 2

all_features = dataset.get_all_data('../feature_data_6_n_20bin.xlsx')

database_filepath = np.asarray(all_features)[:, -1:]
database_features = np.asarray(all_features)[:, :-1].astype(float)

a1_f = database_features[:, 0:5]
a1_rt = annoy(a1_f[q], a1_f)

first = []
for i in range(5):
    d = database_features[:, (i*20+5):(i*20+25)]
    second = annoy(d[q], d)
    first = first + list(set(second) - set(first))
#    print(first)
#    print(second)
#    print(set(second))

result = np.intersect1d(a1_rt, first)
# print(a1_rt)
# print(result)
result = annoy(database_features[q], database_features)

for index in result:
    print(database_filepath[index])
#print(annoy(database_features[0], database_features))