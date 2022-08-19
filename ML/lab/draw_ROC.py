import matplotlib.pyplot as plt
import math
import numpy as np
from sklearn import metrics

tp=int(input('TP='))
tn=int(input('TN='))
fp=int(input('FP='))
fn=int(input('FN='))
label = []
pre = []

for num in range(tp):
	label.append(1)
	pre.append(1)
for num in range(tn):
	label.append(-1)
	pre.append(-1)
for num in range(fp):
	label.append(-1)
	pre.append(1)
for num in range(fn):
	label.append(1)
	pre.append(1)


def AUC(label, pre):
    pos = [i for i in range(len(label)) if label[i] == 1]
    neg = [i for i in range(len(label)) if label[i] == -1]
    auc = 0
    for i in pos:
    	for j in neg:
    		if pre[i] > pre[j]:
    			auc += 1
    		elif pre[i] == pre[j]:
    			auc += 0.5
    return auc / (len(pos)*len(neg))
 
print(AUC(label, pre))
 
from sklearn.metrics import roc_curve, auc
fpr, tpr, th = roc_curve(label, pre , pos_label=1)
print('sklearn', auc(fpr, tpr))


plt.plot(fpr, tpr, th)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.show()
#plt.savefig(path+'\\figure\\'+MHC_ml[t]+'.png')
#plt.clf()