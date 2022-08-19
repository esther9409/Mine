import numpy as np
from sklearn import metrics
import sklearn
from sklearn.metrics import roc_auc_score
import math
import matplotlib.pyplot as plt

y = np.array([0,0,1,1])
pred = np.array([0.1,0.5,0.34,0.8])
print(y)
print(pred)
fpr, tpr, thresholds = metrics.roc_curve(y, pred, pos_label=1)
print(fpr)
print(tpr)
print(thresholds)
auc_out = metrics.auc(fpr, tpr)
auc_out = round(auc_out,4)
print(auc_out)