import matplotlib.pyplot as plt
import math
import numpy as np
from sklearn import metrics
from os import listdir
import re

def auc_curve(y, pred):
	if y == [] or pred == []:
		auc_curve_out = '?'
	else:
		y = np.array(y)
		pred = np.array(pred)
		fpr, tpr, thresholds = metrics.roc_curve(y, pred, pos_label=1)
		auc_curve_out = metrics.auc(fpr, tpr)
		auc_curve_out = round(auc_curve_out,4)
	return fpr, tpr,auc_curve_out

path = '20190422/ROC/'

mine = listdir(path+'mine/')
ann = listdir(path+'ANN 4.0/')
netmhccons = listdir(path+'netMHCcons/')
netmhcpan = listdir(path+'NetMHCpan BA 4.0/')

y = []
pred = []
for t in mine:
	predit = re.compile('.*.predit')
	txt = re.compile('.*.txt')
	if t == 'dl_mlp_result_score.txt':
		mine_file = open(path+'mine/'+t,'r')
		for i in mine_file:
			if i != 'MHC	ans	predict	score\n':
				i = i.strip('\n').split('\t')
				if i[1] == '0':
					y.append(-1)
				elif i[1] == '1':
					y.append(1)
				pred.append(float(i[-1]))
		mine_file.close()
	elif predit.findall(t):
		number = 0
		ans = []
		mine_file = open(path+'mine/'+t,'r')
		file_name = t.split('_T')[0]
		svm_file = open('20190422/ml/Testing_3/normalization/'+file_name+'_Testing_normalization.txt')
		for j in svm_file:
			j = j.split('\t')[0]
			ans.append(int(j))
		for i in mine_file:
			if i != 'labels 1 -1\n':
				i = i.strip('\n').split('\t')
				y.append(ans[number])
				pred.append(float(i[1]))
				number += 1
		mine_file.close()
		svm_file.close()
	elif txt.findall(t):
		number = 0
		mine_file = open(path+'mine/'+t,'r')
		catch = re.compile(r'.*inst#.*')
		for i in mine_file:
			i = i.strip('\n')
			if i == '':
				next
			else:
				if number == 0:
					if catch.findall(i):
						number += 1
				else:
					i = i.split(' ')
					temp = []
					for j in i:
						if j != '':
							temp.append(j)
					if temp[1] == '2:-1' and temp[2] == '2:-1':
						y.append(-1)
						pred.append(1-float(temp[-1]))
					elif temp[1] == '2:-1' and temp[2] == '1:1':
						y.append(-1)
						pred.append(float(temp[-1]))
					elif temp[1] == '1:1' and temp[2] == '2:-1':
						y.append(1)
						pred.append(1-float(temp[-1]))
					elif temp[1] == '1:1' and temp[2] == '1:1': 
						y.append(1)
						pred.append(float(temp[-1]))
		mine_file.close()
fpr, tpr, auc = auc_curve(y, pred)
print(auc)
plt.plot(fpr,tpr)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.savefig(path+'total_comparing_1.png')


y = []
pred = []
for t in ann:
	ann_file = open(path+'ANN 4.0/'+t,'r')
	for i in ann_file:
		i = i.strip('\n').split('\t')
		pred.append(1-(float(i[14])/100))
		y.append(int(i[0]))
	ann_file.close()
fpr_2, tpr_2, auc = auc_curve(y, pred)
print(auc)
plt.plot(fpr_2, tpr_2)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.savefig(path+'total_comparing_2.png')


y = []
pred = []
for t in netmhccons:
	netmhccons_file = open(path+'netMHCcons/'+t,'r')
	for i in netmhccons_file:
		i = i.strip('\n').split('\t')
		pred.append(1-(float(i[7])/100))
		y.append(int(i[0]))
	netmhccons_file.close()
fpr_3, tpr_3, auc = auc_curve(y, pred)
print(auc)
plt.plot(fpr_3, tpr_3)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.savefig(path+'total_comparing_3.png')


y = []
pred = []
for t in netmhcpan:
	netmhcpan_file = open(path+'NetMHCpan BA 4.0/'+t,'r')
	for i in netmhcpan_file:
		i = i.strip('\n').split('\t')
		pred.append(1-(float(i[14])/100))
		y.append(int(i[0]))
	netmhcpan_file.close()
fpr_4, tpr_4, auc = auc_curve(y, pred)
print(auc)
plt.plot(fpr_4, tpr_4)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.savefig(path+'total_comparing.png')
plt.show()
