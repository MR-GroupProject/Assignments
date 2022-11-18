import os
import numpy as np
from annoy import AnnoyIndex

from tools import dataset
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
    def __init__(self, q_path, d_path='../data/feature_data_6_n_20bin.xlsx'):
        self.descriptors_results = {}
        self.distance_results = {}
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
        results = []
        for i in range(6):
            results.append(compare_feature(self.q_cont_f[i], d_f[:, i], method=1))
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
        self.distance_results = {}
        self.descriptors_results = {}
        a3, d1, d2, d3, d4 = self.get_hist_distance(self.data_features)
        a3 = normalize.normalization(a3)
        d1 = normalize.normalization(d1)
        d2 = normalize.normalization(d2)
        d3 = normalize.normalization(d3)
        d4 = normalize.normalization(d4)
        const_dist = self.get_const_distance(self.d_const_f_std)
        for i in range(6):
            const_dist[i] = normalize.normalization(const_dist[i])

        for i in range(len(self.data_features)):
            # final_dis = a3[i] * 0.15 + d1[i] * 0.15 + d2[i] * 0.4 + d3[i] * 0.15 + d4[i] * 0.15
            # final_dis = final_dis * 0.9 + const_dist[i] * 0.1
            final_dis = (a3[i] + d1[i] + d2[i] + d3[i] + d4[i] + const_dist[0][i] + const_dist[1][i] + const_dist[2][i]
                         + const_dist[3][i] + const_dist[4][i] + const_dist[5][i]) / 11
            self.distance_results.update({i: final_dis})
            self.descriptors_results.update({i: [a3[i], d1[i], d2[i], d3[i], d4[i]]})

        sorted_dis = sorted(self.distance_results.items(), key=lambda x: x[1])
        files = []
        class_result = []
        descriptors = []
        distances = []
        for dis in sorted_dis:
            if k == 0:
                break
            filepath = self.data_filepath[dis[0]]
            if filepath[0] != self.q_path:
                descriptors.append(self.descriptors_results.get(dis[0]))
                distances.append(dis[1])
                files.append(filepath[0])
                dir_path = os.path.dirname(filepath[0])
                class_result.append(os.path.basename(dir_path))
                k -= 1

        return files, class_result, descriptors, distances

    def match_by_annoy(self, k=10, t=10):
        tree = AnnoyIndex(len(self.q_features), 'euclidean')  # Length of item vector that will be indexed
        i = 0
        for f in self.data_features:
            tree.add_item(i, f)
            i += 1

        tree.build(t)  # set number of trees
        tree.save('annoy.ann')

        u = AnnoyIndex(len(self.q_features), 'euclidean')
        u.load('annoy.ann')  # fast, just mmap the file
        index = u.get_nns_by_vector(self.q_features, k + 1)  # will find the k nearest neighbors
        matches = []
        for i in index:
            if self.data_filepath[i][0] == self.q_path:
                continue
            matches.append(self.data_filepath[i][0])
        return matches

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

