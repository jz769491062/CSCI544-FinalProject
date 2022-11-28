import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support
import sklearn.metrics as metrics
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import accuracy_score
import numpy as np
import math
from sklearn.metrics import confusion_matrix

df = pd.read_csv("eval_BOW.csv")
pre_list = list(df['y_pred'])
y_list = list(df['y_test'])

def precision_recall_score(pre_list, y_list):
    lr_precision, lr_recall, _ = precision_recall_curve(pre_list, y_list)
    # plt.plot(lr_recall, lr_precision, marker='.', label='Logistic')
    # plt.xlabel('Recall')
    # plt.ylabel('Precision')
    # plt.show()
    return precision_recall_fscore_support(pre_list, y_list)[0], precision_recall_fscore_support(pre_list, y_list)[1]    

def f_score(pre_list, y_list):
    return precision_recall_fscore_support(pre_list, y_list)[2]

def auc_score(pre_list, y_list):
    fpr, tpr, threshold = metrics.roc_curve(pre_list, y_list)
    roc_auc = metrics.auc(fpr, tpr)

    # plt.title('Receiver Operating Characteristic')
    # plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
    # plt.legend(loc = 'lower right')
    # plt.plot([0, 1], [0, 1],'r--')
    # plt.xlim([0, 1])
    # plt.ylim([0, 1])
    # plt.ylabel('True Positive Rate')
    # plt.xlabel('False Positive Rate')
    # plt.show()
    return roc_auc

print("BOW eval:")
print(precision_recall_score(pre_list, y_list)[0].mean())
print(precision_recall_score(pre_list, y_list)[1].mean())
print(f_score(pre_list, y_list).mean())
print(accuracy_score(pre_list, y_list))
print(auc_score(pre_list, y_list))

df = pd.read_csv("eval_TFIDF.csv")
pre_list = list(df['y_pred'])
y_list = list(df['y_test'])
original_sentiment = list(df['original_sentiment'])

print("TFIDF eval:")
print(precision_recall_score(pre_list, y_list)[0].mean())
print(precision_recall_score(pre_list, y_list)[1].mean())
print(f_score(pre_list, y_list).mean())
print(accuracy_score(pre_list, y_list))
print(auc_score(pre_list, y_list))
# diff_list = []
# for pre, y in zip(pre_list, y_list):
#     diff_list.append(abs(pre - y))
bins = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
bins_count = [0 for i in range(0, 10)]
bins_count_all = [0 for i in range(0, 10)]
for index, i in enumerate(original_sentiment):
    bins_count_all[math.floor(i * 10)] = bins_count_all[math.floor(i * 10)] + 1
    if pre_list[index] - y_list[index] != 0:
        bins_count[math.floor(i * 10)] = bins_count[math.floor(i * 10)] + 1

for index in range(len(bins_count)):
    bins_count[index] = 1.0 * bins_count[index] / bins_count_all[index]

plt.title("Error Rate by Sentiment Score")
plt.xlabel("Sentiment Score")
plt.ylabel("Error Rate")
plt.plot(bins, bins_count, linestyle = 'dotted')
plt.show()


        