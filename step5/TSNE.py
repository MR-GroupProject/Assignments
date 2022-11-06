from tools import distance, reader
from tools import dataset, normalize
import numpy as np
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE

all_features = dataset.get_all_data('../feature_data_6_n_20bin.xlsx')
database_features = np.asarray(all_features)[:, :-1].astype(float)
const_features = database_features[:, :6]
normed_features = normalize.standardization(const_features)
database_features[:, :6] = normed_features


def dist(row1, row2):
    const_col1 = row1[:6]
    const_col2 = row2[:6]
    dist1 = distance.euc(const_col1, const_col2)
    hist_dist = []
    dist2 = 0
    for k in range(5):
        hist_col1 = row1[(k * 20 + 6):(k * 20 + 26)]
        hist_col2 = row2[(k * 20 + 6):(k * 20 + 26)]
        hist_dist.append(distance.EMD(hist_col1, hist_col2, 20))
        dist2 += hist_dist[k]
    return (dist1 + dist2) / 6


X_embedded = TSNE(n_components=2, learning_rate=500, method='exact', early_exaggeration=1,
                  init='pca', metric=dist, perplexity=20, n_iter=1000, verbose=1).fit_transform(database_features)

# X_embedded = TSNE(n_components=2, learning_rate=45, method='exact',
#                    init='pca', metric=dist, perplexity=20, n_iter=1000).fit_transform(database_features)

# X_embedded = TSNE(n_components=2, learning_rate=45,
#                   init='pca', metric='euclidean', perplexity=20, n_iter=1000).fit_transform(database_features)


x_min, x_max = X_embedded.min(0), X_embedded.max(0)
x_norm = (X_embedded - x_min) / (x_max - x_min)

obj_types = reader.read_sub_fold()
fig = plt.figure(figsize=(10, 8))
for i in range(19):
    plt.scatter(x_norm[i * 20:(i + 1) * 20, 0], x_norm[i * 20:(i + 1) * 20, 1], s=60,
                color=plt.cm.tab20(i), label=obj_types[i])
plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)
plt.title("t-SNE DR Scatter Plot")
fig.subplots_adjust(right=0.8)
# plt.show()
fig.savefig("../Visualization/tsne.pdf")
