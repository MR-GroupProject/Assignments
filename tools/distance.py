import numpy as np
from scipy.spatial import distance
from scipy.stats import wasserstein_distance


def euc(a, b):
    return distance.euclidean(a, b)


def co(a, b):
    return distance.cosine(a, b)


def EMD(a, b, length):
    t = np.array(range(length))
    return wasserstein_distance(t, t, a, b)
