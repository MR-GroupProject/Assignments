import joblib
import json
import numpy as np
from tools import reader

from sklearn import neighbors

def train(root, dist_metric):

    data_X = []
    data_Y = []

    obj_types = reader.read_sub_fold(root)

    for obj_type in obj_types:
        file_paths = reader.read_file(root, obj_type, "json")
        for file in file_paths:
            with open(file, 'r') as f:
                data = json.load(f)
            data_X.append(data[root])
            data_Y.append(data["class"])

    data_X = np.asarray(data_X)
    data_Y = np.asarray(data_Y)



    train_X = data_X
    train_Y = data_Y

    # indeces = np.random.permutation(len(data_X))

    # train_X = data_X[indeces[:-50]]
    # train_Y = data_Y[indeces[:-50]]

    # test_X = data_X[indeces[-50:]]
    # test_Y = data_Y[indeces[-50:]]

    knn = neighbors.KNeighborsClassifier(n_neighbors=6,
                                        weights='uniform', algorithm='auto', leaf_size=30,
                                        metric=dist_metric, metric_params=None, n_jobs=-1)
    '''
        @param n_neighbors: 指定kNN的k值
        @param weights:  
        'uniform': 本节点的所有邻居节点的投票权重都相等
        'distance': 本节点的所有邻居节点的投票权重与距离成反比
        @param algorithm:  惩罚项系数的倒数，越大，正则化项越小
        'ball_tree': BallTree算法
        'kd_tree': kd树算法
        'brute': 暴力搜索算法 
        'auto': 自动决定适合的算法
        @param leaf_size:  指定ball_tree或kd_tree的叶节点规模。他影响树的构建和查询速度
        @param p:  p=1:曼哈顿距离; p=2:欧式距离
        @param metric:  指定距离度量，默认为'minkowski'距离
        @param n_jobs: 任务并行时指定使用的CPU数，-1表示使用所有可用的CPU

        @method fit(X,y): 训练模型
        @method predict(X): 预测
        @method score(X,y): 计算在(X,y)上的预测的准确率
        @method predict_proba(X): 返回X预测为各类别的概率
        @method kneighbors(X, n_neighbors, return_distance): 返回样本点的k近邻点。如果return_distance=True，则也会返回这些点的距离
        @method kneighbors_graph(X, n_neighbors, mode): 返回样本点的连接图
    '''

    knn.fit(train_X, train_Y)

    joblib.dump(knn, root+"_"+dist_metric.__name__+".pkl")

# train("D4", distance.EMD)
