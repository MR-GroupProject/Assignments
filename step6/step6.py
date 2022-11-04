import os
from step4.matching import Matching


def precision(tp, k=10):
    # PPV = TP / (TP + FP) = TP / s
    return tp / k


def recall(tp):
    # TPR = TP / (TP+FN) = TP / c
    return tp / 19


def acc(tp, tn):
    # ACC = (TP+TN) / (TP+FN+FP+TN) = (TP+TN) / d
    return (tp + tn) / 379


def evaluate(d_f, k=10):
    result = []
    for data in d_f:
        p = data[-1:]
        c = os.path.basename(os.path.dirname(p))
        m = Matching(p)
        matches, classes, descriptors, distances = m.match(k=k)
        tp, fp, tn, fn = 0, 0, 0, 0
        for match in matches:
            m_c = os.path.basename(os.path.dirname(match))
            if m_c == c:
                tp += 1
            else:
                fp += 1
        fn = 19 - tp
        tn = 379 - 19 - fp
        result.append([tp, fp, tn, fn])
    return result


'''class Evaluation:
    def __init__(self, d_path='../feature_data_6_20bin.xlsx'):
        self.d_path = d_path'''
