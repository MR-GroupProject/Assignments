import time
import matplotlib.pyplot as plt
import numpy as np

from step4 import matching


q_mesh = "../Remesh/Ant/82.off"
m = matching.Matching(q_mesh)

k_ = []
a_ = []
for j in range(5):
    knn = []
    ann = []
    k = 0
    for i in range(6):
        k = k + 5

        start = time.time()
        m.match(k=k)
        end = time.time()
        knn.append(end-start)

        start = time.time()
        m.match_by_annoy(k=k)
        end = time.time()
        ann.append(end-start)
    k_.append(knn)
    a_.append(ann)

x = np.array([5, 10, 15, 20, 25, 30])
k_mean = np.mean(np.asarray(k_), axis=0)
a_mean = np.mean(np.asarray(a_), axis=0)
fig = plt.figure(figsize=(6, 4))
plt.plot(x, k_mean, label='k-NN')
plt.plot(x, a_mean, label='ANN')
plt.xlabel("k value")
plt.ylabel("Average time spent(seconds)")
plt.title("Average Querying Time")
plt.legend()
# plt.show()
fig.savefig("../Visualization/roc/timer.png")
