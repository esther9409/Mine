import gc
import math
import numpy as np
from sklearn import metrics
from os import listdir
import re
import matplotlib.pyplot as plt

def acc(tp,tn,fp,fn):
	if (tp+tn+fp+fn) == 0:
		acc_out = '?'
	else:
		acc_out = (tp+tn)/(tp+tn+fp+fn)
		acc_out = round(acc_out,4)
	return acc_out

def mcc(tp,tn,fp,fn):
	if (math.sqrt((tp+fn)*(fp+tn)*(tp+fp)*(fn+tn))) == 0:
		mcc_out = '?'
	else:
		mcc_out = ((tp*tn)-(fp*fn))/math.sqrt((tp+fn)*(fp+tn)*(tp+fp)*(fn+tn))
		mcc_out = round(mcc_out,4)
	return mcc_out

def f1(tp,fn,fp):
	if (tp+fn+tp+fp) == 0:
		f1_out = '?'
	else:
		f1_out = 2*tp/(tp+fn+tp+fp)
		f1_out = round(f1_out,4)
	return f1_out

def Sn(tp,fn):
	if (tp+fn) == 0:
		Sn_out = '?'
	else:
		Sn_out = tp/(tp+fn)
		Sn_out = round(Sn_out,4)
	return Sn_out

def Sp(tn,fp):
	if (fp+tn) == 0:
		Sp_out = '?'
	else:
		Sp_out = tn/(fp+tn)
		Sp_out = round(Sp_out,4)
	return Sp_out

def auc_curve(y, pred):
	if y == [] or pred == []:
		auc_curve_out = '?'
	else:
		y = np.array(y)
		pred = np.array(pred)
		fpr, tpr, thresholds = metrics.roc_curve(y, pred, pos_label=1)
		auc_curve_out = metrics.auc(fpr, tpr)
		auc_curve_out = round(auc_curve_out,4)
	return auc_curve_out

asml_ind_output = open('20190422/weka_asml_ind_result.txt','a')
asml_ind_output.write('MHC\tclassifier\tTP\tTN\tFP\tFN\tSn\tSp\tAcc\tMCC\tAUC\tF1\n')
asml_cv_output = open('20190422/weka_asml_cv_result.txt','a')
asml_cv_output.write('MHC\tclassifier\tTP\tTN\tFP\tFN\tSn\tSp\tAcc\tMCC\tAUC\tF1\n')

weka_path = 'C:/Users/NCBLAB/Desktop/weka_result/'
weka = listdir(weka_path)
key_cv = re.compile(r'.*_cv_.*')
key_ind = re.compile(r'.*_ind_.*')
for t in range(len(weka)):
	if key_cv.findall(weka[t]):
		file_name = weka[t].split('_cv_')[0]
		classifier_name = weka[t].split('_cv_')[1]
		weka_input = open(weka_path+weka[t],'r')
		tp = 0
		fp = 0
		tn = 0
		fn = 0
		y = []
		pred = []
		number = 0
		for i in weka_input:
			i = i.strip('\n')
			catch = re.compile(r'.*inst#.*')
			if i == '':
				next
			else:
				if number == 0:
					if catch.findall(i):
						number += 1
				else:
					i = i.strip('\n').split(' ')
					temp = []
					for j in i:
						if j != '':
							temp.append(j)
					if temp[1] == '2:-1' and temp[2] == '2:-1':
						tn += 1
						y.append(-1)
						pred.append(1-float(temp[-1]))
					elif temp[1] == '2:-1' and temp[2] == '1:1':
						fp += 1
						y.append(-1)
						pred.append(float(temp[-1]))
					elif temp[1] == '1:1' and temp[2] == '2:-1':
						fn += 1
						y.append(1)
						pred.append(1-float(temp[-1]))
					elif temp[1] == '1:1' and temp[2] == '1:1':
						tp += 1
						y.append(1)
						pred.append(float(temp[-1]))
		asml_cv_output.write(file_name+'\t')
		asml_cv_output.write(classifier_name+'\t')
		asml_cv_output.write(str(tp)+'\t')
		asml_cv_output.write(str(tn)+'\t')
		asml_cv_output.write(str(fp)+'\t')
		asml_cv_output.write(str(fn)+'\t')
		asml_cv_output.write(str(Sn(tp,fn))+'\t')
		asml_cv_output.write(str(Sp(tn,fp))+'\t')
		asml_cv_output.write(str(acc(tp,tn,fp,fn))+'\t')
		asml_cv_output.write(str(mcc(tp,tn,fp,fn))+'\t')
		asml_cv_output.write(str(auc_curve(y, pred))+'\t')
		asml_cv_output.write(str(f1(tp,fn,fp))+'\n')
		weka_input.close()
		
	elif key_ind.findall(weka[t]):
		file_name = weka[t].split('_ind_')[0]
		classifier_name = weka[t].split('_ind_')[1]
		weka_input = open(weka_path+weka[t],'r')
		tp = 0
		fp = 0
		tn = 0
		fn = 0
		y = []
		pred = []
		number = 0
		for i in weka_input:
			i = i.strip('\n')
			catch = re.compile(r'.*inst#.*')
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
					print(i)
					print(len(temp))
					if temp[1] == '2:-1' and temp[2] == '2:-1':
						tn += 1
						y.append(-1)
						pred.append(1-float(temp[-1]))
					elif temp[1] == '2:-1' and temp[2] == '1:1':
						fp += 1
						y.append(-1)
						pred.append(float(temp[-1]))
					elif temp[1] == '1:1' and temp[2] == '2:-1':
						fn += 1
						y.append(1)
						pred.append(1-float(temp[-1]))
					elif temp[1] == '1:1' and temp[2] == '1:1':
						tp += 1
						y.append(1)
						pred.append(float(temp[-1]))
		asml_ind_output.write(file_name+'\t')
		asml_ind_output.write(classifier_name+'\t')
		asml_ind_output.write(str(tp)+'\t')
		asml_ind_output.write(str(tn)+'\t')
		asml_ind_output.write(str(fp)+'\t')
		asml_ind_output.write(str(fn)+'\t')
		asml_ind_output.write(str(Sn(tp,fn))+'\t')
		asml_ind_output.write(str(Sp(tn,fp))+'\t')
		asml_ind_output.write(str(acc(tp,tn,fp,fn))+'\t')
		asml_ind_output.write(str(mcc(tp,tn,fp,fn))+'\t')
		asml_ind_output.write(str(auc_curve(y, pred))+'\t')
		asml_ind_output.write(str(f1(tp,fn,fp))+'\n')
		weka_input.close()

asml_ind_output.close()
asml_cv_output.close()