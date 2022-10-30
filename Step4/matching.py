import os
import numpy as np
from scipy.spatial import distance
from scipy.stats import wasserstein_distance

from tools import dataset, reader
from tools import normalize
from Step3 import features as ft


def euc(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.linalg.norm(a - b)


def co(a, b):
    return distance.cosine(a, b)


def EMD(a, b, length):
    t = np.array(range(length))
    return wasserstein_distance(t, t, a, b)


def compare_feature(query_feature, database, method=0, length=20):
    distance_set = []
    dist = 0
    for data in database:
        if method == 0:
            dist = EMD(query_feature, data, length=length)
        elif method == 1:
            dist = euc(query_feature, data)
        elif method == 2:
            dist = co(query_feature, data)
        distance_set.append(dist)
    # print(result)

    return distance_set


'''
get distances for one descriptor
'''


def get_single_distance(query_feature, database_features, start_col, end_col, method):
    features = database_features[:, start_col:end_col]  # get data columns for the descriptor
    query = query_feature[:, start_col:end_col]
    query = query[0]

    results = compare_feature(query, features, method=method)
    return results


'''
get distance for all single-value features: 
[area, compactness, rectangularity, diameter, eccentricity]
'''


def get_cont_distance(query_path, database_features, database_filepath):
    const_features = database_features[:, :5]  # get data columns for single-value features
    normed_features = normalize.standardization(const_features)
    index = 0
    for path in database_filepath:
        if path == query_path:
            break
        index += 1
    qef_const_feature = normed_features[index]
    print(index)
    results = compare_feature(qef_const_feature, normed_features, method=1)
    return results


def get_hist_distance(query_features, database_features):
    a3_result = []
    d1_result = []
    d2_result = []
    d3_result = []
    d4_result = []
    for i in range(5):
        d = database_features[:, (i * 20 + 5):(i * 20 + 25)]
        d_q = np.asarray(query_features)[(i * 20 + 5):(i * 20 + 25)]
        if i == 0:
            a3_result = compare_feature(d_q, d, method=0)
        elif i == 1:
            d1_result = compare_feature(d_q, d, method=0)
        if i == 2:
            d2_result = compare_feature(d_q, d, method=0)
        if i == 3:
            d3_result = compare_feature(d_q, d, method=0)
        if i == 4:
            d4_result = compare_feature(d_q, d, method=0)

    return a3_result, d1_result, d2_result, d3_result, d4_result


def read_database(database='../feature_data_modified_20bin.xlsx'):
    all_features = dataset.get_all_data(database)
    data_filepath = np.asarray(all_features)[:, -1:]
    data_features = np.asarray(all_features)[:, :-1].astype(float)
    return data_filepath, data_features


def match(query_path, k=10):
    database_filepath, database_features = read_database()
    qef = ft.get_feature(query_path)

    a3, d1, d2, d3, d4 = get_hist_distance(qef, database_features)
    const_dist_results = get_cont_distance(query_path, database_features, database_filepath)

    distance_results = {}
    for i in range(len(database_features)):
        # final_dis = a3[i] * 0.1 + d1[i] * 0.5 + d2[i] * 0.15 + d3[i] * 0.1 + d4[i] * 0.15
        # final_dis = final_dis * 0.85 + const_dist_results[i] * 0.15
        final_dis = a3[i] + d1[i] + d2[i] + d3[i] + d4[i] + const_dist_results[i]
        distance_results.update({i: final_dis})

    sorted_dis = sorted(distance_results.items(), key=lambda x: x[1])
    result = []
    class_result = []
    for dis in sorted_dis:
        if k == 0:
            break
        filepath = str(database_filepath[dis[0]])
        if filepath != ('[\'' + query_path + '\']'):
            result.append(filepath)
            # print(filepath)
            dir_path = os.path.dirname(filepath)
            class_result.append(os.path.basename(dir_path))
            # print(class_path)
            k -= 1

    return result, class_result


def distance_all(descriptor=0):
    database_filepath, database_features = read_database()
    const_features = database_features[:, :5]
    database_features[:, :5] = normalize.standardization(const_features)
    distances = []
    if descriptor < 5:
        start = descriptor
        end = start + 1
        m = 1
    elif descriptor == 10:
        start = 0
        end = start + 5
        m = 1
    else:
        start = (descriptor - 5) * 20 + 5  # 5, 25, 45...
        end = start + 20
        m = 0
    for i in range(len(database_features)):  # 380
        distances.extend(get_single_distance(database_features[i:i + 1, :], database_features[i + 1:, :],
                                             start, end, m))

    return distances


'''dist_data_row = []
for i in range(11):
#    print(min(distance_all(i)), max(distance_all(i)))
    d = np.asarray(distance_all(i))
    dt = normalize.standardization(d.T)
    dist_data_row.append(dt)'''

query_path = '../Remesh/Airplane/61.off'
result_, classes_ = match(query_path)
print(result_)
