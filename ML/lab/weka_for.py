import sys
import subprocess
import gc
import time

number = open('C:/Users/NCBLAB/Desktop/research/20190422/number_allele_specific_ml.txt','r')
classifier = open('C:/Users/NCBLAB/Desktop/research/20190422/weka_classifier.txt','r')

MHC_ml = []
for i in number:
	ii = i.split('\t')
	mhc = ii[0].replace(':','_')
	mhc = mhc.replace('*','_')
	MHC_ml.append(mhc)
gc.collect()
number.close()

for num in range(14,len(MHC_ml)):
	train = 'C:/Users/NCBLAB/Desktop/research/20190422/ml/Training_3/all/weka/'+MHC_ml[num]+'_Training.arff'
	Test = 'C:/Users/NCBLAB/Desktop/research/20190422/ml/Testing_3/weka/'+MHC_ml[num]+'_Testing.arff'
	cross_validation = 'C:/Users/NCBLAB/Desktop/weka_result/'+MHC_ml[num]+'_cv_'
	independent_test = 'C:/Users/NCBLAB/Desktop/weka_result/'+MHC_ml[num]+'_ind_'
	model = 'C:/Users/NCBLAB/Desktop/research/20190422/ml/model/weka/'+MHC_ml[num]+'_'
	for line in classifier:
		line = line.strip('\n')
		line_split = line.split('\t')
		try:
			sys.dont_write_bytecode = True
			cmd = 'java -cp "C:\Program Files\Weka-3-8\weka.jar" weka.Run '+line_split[0]+' -t '+train+' -d '+model+line_split[1]+'.model -classifications weka.classifiers.evaluation.output.prediction.PlainText -T '+Test+' > '+independent_test+line_split[1]+'.txt'
			subprocess.call(cmd, shell=True)
			sys.dont_write_bytecode = True
			cmd = 'java -cp "C:\Program Files\Weka-3-8\weka.jar" weka.Run '+line_split[0]+' -x 10 -t '+train+' -classifications weka.classifiers.evaluation.output.prediction.PlainText > '+cross_validation+line_split[1]+'.txt'
			subprocess.call(cmd, shell=True)	
		except:
			print('cannot run')
		gc.collect()
	classifier.seek(0,0)