import os

import numpy as np
from tools import reader

from step4.matching import Matching
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from sklearn.metrics import roc_curve, auc

from tools import dataset


def precision(tp, k=10):
    # PPV = TP / (TP + FP) = TP / s
    return tp / k


def recall(tp, fn):
    # TPR = TP / (TP+FN) = TP / c
    return tp / (tp + fn)


def acc(tp, tn):
    # ACC = (TP+TN) / (TP+FN+FP+TN) = (TP+TN) / d
    return (tp + tn) / 379


def sen(tp, fn):
    # Sensitivity = TP/(TP+FN)
    return recall(tp, fn)


def spec(fp, tn):
    # Specificity = TN/(FP+TN)
    return tn / (fp + tn)


def roc_auc(d_path='../feature_data_6_n_20bin.xlsx', k=380):
    d_f = dataset.get_all_data(d_path)
    all_tpr = []
    all_fpr = []

    for data in d_f:
        p = data[-1:]
        c = os.path.basename(os.path.dirname(p[0]))
        print(c)
        m = Matching(p[0])
        matches, classes, descriptors, distances = m.match(k=k)
        tp, fp = 0, 0
        tpr = []
        fpr = []
        i = 0
        for match in matches:
            m_c = os.path.basename(os.path.dirname(match))

            if m_c == c:
                tp += 1
            else:
                fp += 1
            i += 1
            if i == 2:
                tpr.append(tp)
                fpr.append(fp)
                i = 0
        all_tpr.append(tpr)
        all_fpr.append(fpr)

        # fn = 19 - tp
        # tn = 379 - 19 - fp
    return all_tpr, all_fpr


def draw_roc_per_class():
    # t, f = roc_auc()
    t = dataset.get_all_data('../evaluationt.xlsx')
    f = dataset.get_all_data('../evaluationf.xlsx')
    class_num = np.full((380, 189), 19)
    shape_num = np.full((380, 189), 360)
    t = t / class_num
    f = f / shape_num
    obj_types = reader.read_sub_fold()
    fig = plt.figure(figsize=(8, 8))
    plt.xlabel("FPR (False Positive Rate)")
    plt.ylabel("TPR (True Positive Rate)")
    plt.title("Receiver Operating Characteristic")
    plt.plot([0, 1], [0, 1], markeredgecolor='r', linestyle='--', markerfacecolor='none', color='black')
    # cm = plt.get_cmap('jet')
    # cNorm = colors.Normalize(vmin=0, vmax=20)
    # scalarMap = plt.cm.ScalarMappable(norm=cNorm, cmap=cm)
    for i in range(19):
        class_tpr = np.asarray(t)[i * 20:(i + 1) * 20, :]
        class_fpr = np.asarray(f)[i * 20:(i + 1) * 20, :]
        avg_c_tpr = np.mean(class_tpr, axis=0)
        avg_c_fpr = np.mean(class_fpr, axis=0)
        avg_c_tpr = np.insert(avg_c_tpr, 0, 0)
        avg_c_fpr = np.insert(avg_c_fpr, 0, 0)
        a = auc(avg_c_fpr, avg_c_tpr)
        plt.plot(avg_c_fpr, avg_c_tpr, label=obj_types[i] + ('(auc = %0.2f)' % a), c=plt.cm.tab20(i))

    plt.legend()
    # plt.show()
    fig.savefig("../Visualization/ROC.pdf")


def draw_roc():
    t = dataset.get_all_data('../evaluationt.xlsx')
    f = dataset.get_all_data('../evaluationf.xlsx')
    class_num = np.full((380, 189), 19)
    shape_num = np.full((380, 189), 360)
    t = t / class_num
    f = f / shape_num

    fig = plt.figure(figsize=(8, 8))
    plt.xlabel("FPR (False Positive Rate)")
    plt.ylabel("TPR (True Positive Rate)")
    plt.plot([0, 1], [0, 1], markeredgecolor='r', linestyle='--', markerfacecolor='none', color='black')

    avg_c_tpr = np.mean(np.asarray(t), axis=0)
    avg_c_fpr = np.mean(np.asarray(f), axis=0)
    avg_c_tpr = np.insert(avg_c_tpr, 0, 0)
    avg_c_fpr = np.insert(avg_c_fpr, 0, 0)
    a = auc(avg_c_fpr, avg_c_tpr)
    plt.plot(avg_c_fpr, avg_c_tpr)
    plt.title("Receiver Operating Characteristic(auc = %0.2f)" % a)

    # plt.show()
    fig.savefig("../Visualization/ROC_all.pdf")


'''t, f = roc_auc()
wb, ws = dataset.create_table('../evaluationf.xlsx')
dataset.write_data(f, ws)
wb.close()

wb, ws = dataset.create_table('../evaluationt.xlsx')
dataset.write_data(t, ws)
wb.close()'''

draw_roc()
draw_roc_per_class()
