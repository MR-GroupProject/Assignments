from tools import dataset
import numpy as np
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE

all_features = dataset.get_all_data('../feature_data_normed.xlsx')

database_features = np.asarray(all_features)[:, :-1].astype(float)
database_features = database_features[:,:5]


X = database_features
X_embedded = TSNE(n_components=2,
                  init='pca', perplexity=30, n_iter=1000 ,verbose=1).fit_transform(X)

x_min, x_max = X_embedded.min(0), X_embedded.max(0)
x_norm = (X_embedded-x_min)/(x_max-x_min)

label = []
for i in range (0, 19):
    clss = [i for j in range(20)]
    label.extend(clss)

plt.figure(figsize=(8,8))
for i in range(x_norm.shape[0]):
    plt.text(x_norm[i, 0], x_norm[i, 1], str(label[i]), color=plt.cm.Set1(label[i]), fontdict = {'weight': 'bold', 'size':9})

plt.xticks([])
plt.yticks([])
plt.show()


'''
#print(X_embedded)
x = X_embedded[:,0]
y = X_embedded[:,1]

#print(x)
#print(y)

label = []
for i in range (0, 19):
    clss = [i for j in range(20)]
    label.extend(clss)

a = matplotlib.pyplot
#a.ion()
'''
'''
for i in range (0, 19):
    x = X_embedded[i*20:i*20+19, 0]
    y = X_embedded[i*20:i*20+19, 1]
'''

'''

a.scatter(x, y, s=2.5, c=label, label = label)
    #a.draw()
    #a.pause(1.5)
a.show()
'''