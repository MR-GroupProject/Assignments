import os
import numpy as np

from tools import dataset, reader
from tools import distance as dist
from tools import normalize
from step3 import features as ft


def compare_feature(query_feature, database, method=0, length=20):
    distance_set = []
    d = 0
    for data in database:
        if method == 0:
            d = dist.EMD(query_feature, data, length=length)
        elif method == 1:
            d = dist.euc(query_feature, data)
        elif method == 2:
            d = dist.co(query_feature, data)
        distance_set.append(d)
    return distance_set


class Matching:
    def __init__(self, q_path, d_path='../feature_data_6_n_20bin.xlsx'):
        self.q_path = q_path
        self.d_path = d_path

        all_features = dataset.get_all_data(self.d_path)
        self.data_filepath = np.asarray(all_features)[:, -1:]
        self.data_features = np.asarray(all_features)[:, :-1].astype(float)
        self.d_const_f_std = self.get_d_const_f_standardize()

        self.q_features = self.get_q_f()
        self.q_cont_f = self.get_q_const_f(self.q_path)
        self.q_hist_f = self.get_q_hist_f()

    def get_d_const_f_standardize(self):
        const_features = self.data_features[:, :6]  # get data columns for single-value features
        normed_features = normalize.standardization(const_features)
        return normed_features

    def get_q_f(self):
        return ft.get_feature(self.q_path)

    def get_q_const_f(self, path):
        index = 0
        is_in_db = False  # whether the query mesh q is in database
        # if the query mesh is from database, get single-value features of q from the dataset directly
        # if not, standardize q and database feature values
        for p in self.data_filepath:
            if p == path:
                is_in_db = True
                break
            index += 1
        if is_in_db:
            return self.d_const_f_std[index]
        else:
            const_f = self.data_features[:, :6]
            q_f = np.asarray(self.q_features).reshape(1, -1)
            const_f = np.append(const_f, q_f[:, :6], axis=0)
            normed_f = normalize.standardization(const_f)
            return normed_f[-1:, :]

    def get_q_hist_f(self):
        f = []
        for i in range(6):
            f.append(np.asarray(self.q_features)[(i * 20 + 6):(i * 20 + 26)])
        return f

    def get_hist_distance(self, d_f):
        a3_result = []
        d1_result = []
        d2_result = []
        d3_result = []
        d4_result = []
        for i in range(5):
            d = d_f[:, (i * 20 + 6):(i * 20 + 26)]
            d_q = self.q_hist_f[i]
            if i == 0:
                a3_result = compare_feature(d_q, d, method=0)
            elif i == 1:
                d1_result = compare_feature(d_q, d, method=0)
            elif i == 2:
                d2_result = compare_feature(d_q, d, method=0)
            elif i == 3:
                d3_result = compare_feature(d_q, d, method=0)
            elif i == 4:
                d4_result = compare_feature(d_q, d, method=0)

        return a3_result, d1_result, d2_result, d3_result, d4_result

    def get_const_distance(self, d_f):
        """
        To get feature distance for all single-value descriptors:
        [area, compactness, rectangularity, diameter, eccentricity]
        """
        results = compare_feature(self.q_cont_f, d_f, method=1)
        return results

    def match(self, k=10):
        """
        matching function
        Returns:
            files - the filepath of result meshes
            class_result - the shape classification of result meshes
            descriptors - the descriptors of result meshes
            distances - the feature distances between query mesh and result meshes
        """
        a3, d1, d2, d3, d4 = self.get_hist_distance(self.data_features)
        const_dist = self.get_const_distance(self.d_const_f_std)
        distance_results = {}
        descriptors_results = {}
        for i in range(len(self.data_features)):
            #final_dis = a3[i] * 0.15 + d1[i] * 0.15 + d2[i] * 0.4 + d3[i] * 0.15 + d4[i] * 0.15
            #final_dis = final_dis * 0.9 + const_dist[i] * 0.1
            final_dis = (a3[i] + d1[i] + d2[i] + d3[i] + d4[i] + const_dist[i]) / 6
            distance_results.update({i: final_dis})
            descriptors_results.update({i: [const_dist[i], a3[i], d1[i], d2[i], d3[i], d4[i]]})

        sorted_dis = sorted(distance_results.items(), key=lambda x: x[1])
        files = []
        class_result = []
        descriptors = []
        distances = []
        for dis in sorted_dis:
            if k == 0:
                break
            filepath = self.data_filepath[dis[0]]
            if filepath[0] != self.q_path:
                descriptors.append(descriptors_results.get(dis[0]))
                distances.append(dis[1])
                files.append(filepath[0])
                dir_path = os.path.dirname(filepath[0])
                class_result.append(os.path.basename(dir_path))
                k -= 1

        return files, class_result, descriptors, distances

    def get_feature_by_path(self, path):
        get = False
        i = 0
        for p in self.data_filepath:
            if p == path:
                get = True
                break
            i += 1
        if not get:
            return None
        else:
            return self.data_features[i]


'''def get_single_distance(query_feature, database_features, start_col, end_col, method):
    """
    To get feature distances for one descriptor
    """
    features = database_features[:, start_col:end_col]  # get data columns for the descriptor
    query = query_feature[:, start_col:end_col]
    query = query[0]

    results = compare_feature(query, features, method=method)
    return results


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

    return distances'''


'''dist_data_row = []
for i in range(11):
#    print(min(distance_all(i)), max(distance_all(i)))
    d = np.asarray(distance_all(i))
    dt = normalize.standardization(d.T)
    dist_data_row.append(dt)'''
