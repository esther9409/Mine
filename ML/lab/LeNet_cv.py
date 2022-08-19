import tensorflow as tf
import numpy as np
from keras import optimizers
from keras.callbacks import Callback, EarlyStopping
from sklearn import metrics
import math
from os import listdir
import sys
import os
import gc
from sklearn.model_selection import StratifiedKFold
from keras.utils.np_utils import to_categorical
seed = 7
seed = np.random.seed(seed)

# gpu_options = tf.GPUOptions(allow_growth=True)
# sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
# tf.keras.backend.set_session(sess)

def mcc(tp,tn,fp,fn):
    if (math.sqrt((tp+fn)*(fp+tn)*(tp+fp)*(fn+tn))) == 0:
        mcc_out = '?'
    else:
        mcc_out = ((tp*tn)-(fp*fn))/math.sqrt((tp+fn)*(fp+tn)*(tp+fp)*(fn+tn))
        mcc_out = round(mcc_out,4)
    return mcc_out
def sp(tn,fp):
    if (fp+tn) == 0:
        sp_out = '?'
    else:
        sp_out = tn/(fp+tn)
        sp_out = round(sp_out,4)
    return sp_out
def sn(tp,fn):
    if (tp+fn) == 0:
        sn_out = '?'
    else:
        sn_out = tp/(tp+fn)
        sn_out = round(sn_out,4)
    return sn_out
def f1(tp,fn,fp):
    if (tp*2+fn+fp) == 0:
        f1_out = '?'
    else:
        f1_out = (tp*2)/(tp*2+fn+fp)
        f1_out = round(f1_out,4)
    return f1_out
def auc(y,pred):
    y = np.array(y)
    pred = np.array(pred)
    fpr, tpr, thresholds = metrics.roc_curve(y, pred, pos_label=1)
    auc_out = metrics.auc(fpr, tpr)
    auc_out = round(auc_out,4)
    return auc_out

#if len(sys.argv) <= 1:
#    print('Usage: {0} training_result_file [training_feature_file] [testing_result_file] [testing_feature_file]'.format(sys.argv[0]))
#    raise SystemExit
#
#train_result_pathname = sys.argv[1]
#train_feature_pathname = sys.argv[2]
#assert os.path.exists(train_result_pathname),"training result file not found"
#assert os.path.exists(train_feature_pathname),"training feature file not found"
#file_name = os.path.split(train_result_pathname)[1]
#
#if len(sys.argv) > 4:
#    test_result_pathname = sys.argv[3]
#    file_name

MHC_dl_read = open('C:\\Users\\allen\\Desktop\\Esther\\number_allele_specific_dl.txt','r')

MHC_dl = []
for j in MHC_dl_read:
    jj = j.split('\t')
    MHC_dl.append(jj[0])
    MHC_dl.append('0')
MHC_dl.append('MHC_pan_allele')
MHC_dl.append('0')
gc.collect()

MHC_dl_read.close()

path="C:\\Users\\allen\\Desktop\\Esther\\dl\\LeNet_cv\\";
model_path="C:\\Users\\allen\\Desktop\\Esther\\dl\\mlp_cv\\model\\";
trian_path="C:\\Users\\allen\\Desktop\\Esther\\dl\\Training\\all\\mlp_cv\\";
test_path="C:\\Users\\allen\\Desktop\\Esther\\dl\\Testing\\mlp\\";


filep=open(path+'dl_LeNet_cv_result.txt',"a")

trian_files = listdir(trian_path)
test_files = listdir(test_path)
y_ans = []
pred = []
tp = 0
tn = 0
fp = 0
fn = 0
filep.write('MHC\tloss\tacc\tauc\tmcc\tf1\tsp\tsn\ttp\tfn\ttn\tfp\n')
filep.close()
filep_2=open(path+'dl_LeNet_cv_result_score.txt',"a")
filep_2.write('MHC\tans\tpredict\tscore\n')
filep_2.close()
for t in range(0,len(MHC_dl),2):
    number = 1
    print(t)
    print(trian_path+trian_files[t])
    x = np.loadtxt(open(trian_path+trian_files[t+1], "rb"), delimiter=",")
    x = np.expand_dims(x, axis=2)
    print(x.shape)

    y = np.loadtxt(open(trian_path+trian_files[t], "rb"), delimiter=",")
#    y = np.expand_dims(y, axis=2)
    print(y.shape)
    
    kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
    cvscores = []
    for train, test in kfold.split(x, y):
        print(number)
        if number == 1:
            y = to_categorical(y, num_classes=None)
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Conv1D(6, 5, activation='tanh', input_shape=(x.shape[1], 1)))
        model.add(tf.keras.layers.AveragePooling1D(2))
        model.add(tf.keras.layers.Conv1D(16, 5, activation='tanh'))
        model.add(tf.keras.layers.AveragePooling1D(2))
        model.add(tf.keras.layers.Conv1D(120, 5, activation='tanh'))
        model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(84, activation='tanh'))
        model.add(tf.keras.layers.Dense(2, activation='softmax'))

        model.compile(loss=tf.keras.losses.categorical_crossentropy,
                  #optimizer=tf.keras.optimizers.Adadelta(lr=0.01, clipnorm=1.),
                  #optimizer=tf.keras.optimizers.Adagrad(lr=0.01, clipnorm=1.),
                  optimizer=tf.keras.optimizers.Adam(lr=0.00001, clipnorm=1.),
                  #optimizer=tf.keras.optimizers.Adamax(lr=0.01, clipnorm=1.),
                  #optimizer=tf.keras.optimizers.Nadam(lr=0.01, clipnorm=1.),             
                  #optimizer=tf.keras.optimizers.RMSprop(lr=0.01, clipnorm=1.),
                  #optimizer=tf.keras.optimizers.SGD(lr=0.01, clipnorm=1.),
                  metrics=['accuracy'])
                  #metrics=[tf.keras.metrics.categorical_accuracy])
        my_callbacks = [EarlyStopping(monitor='val_loss', patience=10, verbose=1, mode='min')]

        # class_weight = {0: 3.,
#                 1: 3.,
#               }
        model.fit(x[train], y[train],
#            validation_split=0.3,
#            shuffle=True,
            batch_size=10,
            epochs=1000,
            verbose=1,
            #class_weight=class_weight,
            validation_data=(x[test], y[test]),
            callbacks=my_callbacks)
        
        results = model.predict(x[test],verbose=0)
        resultsClass2 = model.predict_classes(x[test],verbose=0)
        for num in range(0,len(resultsClass2)):
            if y[test][num][0] == 1.0 and y[test][num][1] == 0.0 and resultsClass2[num] == 0:
                tn += 1
                y_ans.append(0)
                pred.append(results[num][1])
                filep_2=open(path+'dl_LeNet_cv_result_score.txt',"a")
                filep_2.write(MHC_dl[t]+"\t")
                filep_2.write('0'+'\t')
                filep_2.write('0'+'\t')
                filep_2.write(str(results[num][0])+'\t')
                filep_2.write(str(results[num][1])+'\n')
                filep_2.close()
            elif y[test][num][0] == 1.0 and y[test][num][1] == 0.0 and resultsClass2[num] == 1:
                fp += 1
                y_ans.append(0)
                pred.append(results[num][1])
                filep_2=open(path+'dl_LeNet_cv_result_score.txt',"a")
                filep_2.write(MHC_dl[t]+"\t")
                filep_2.write('0'+'\t')
                filep_2.write('1'+'\t')
                filep_2.write(str(results[num][0])+'\t')
                filep_2.write(str(results[num][1])+'\n')
                filep_2.close()
            elif y[test][num][0] == 0.0 and y[test][num][1] == 1.0 and resultsClass2[num] == 1:
                tp += 1
                y_ans.append(1)
                pred.append(results[num][1])
                filep_2=open(path+'dl_LeNet_cv_result_score.txt',"a")
                filep_2.write(MHC_dl[t]+"\t")
                filep_2.write('1'+'\t')
                filep_2.write('1'+'\t')
                filep_2.write(str(results[num][0])+'\t')
                filep_2.write(str(results[num][1])+'\n')
                filep_2.close()
            elif y[test][num][0] == 0.0 and y[test][num][1] == 1.0 and resultsClass2[num] == 0:
                fn += 1
                y_ans.append(1)
                pred.append(results[num][1])
                filep_2=open(path+'dl_LeNet_cv_result_score.txt',"a")
                filep_2.write(MHC_dl[t]+"\t")
                filep_2.write('1'+'\t')
                filep_2.write('0'+'\t')
                filep_2.write(str(results[num][0])+'\t')
                filep_2.write(str(results[num][1])+'\n')
                filep_2.close()
        score = model.evaluate(x[test], y[test], verbose=0)
        filep=open(path+'dl_LeNet_cv_result.txt',"a")
        filep.write(MHC_dl[t]+'\t')
        filep.write(str(round(score[0],4))+"\t")
        filep.write(str(round(score[1],4))+"\t")
        filep.write(str(auc(y_ans,pred))+"\t")
        filep.write(str(mcc(tp,tn,fp,fn))+"\t")
        filep.write(str(f1(tp,fn,fp))+"\t")
        filep.write(str(sp(tn,fp))+"\t")
        filep.write(str(sn(tp,fn))+"\t")
        filep.write(str(tp)+"\t")
        filep.write(str(fn)+"\t")
        filep.write(str(tn)+"\t")
        filep.write(str(fp)+"\n")
        filep.close()
        print('loss:', round(score[0],4))
        print('acc:', round(score[1],4))
        print('auc:', auc(y_ans,pred))
        print('mcc:', mcc(tp,tn,fp,fn))
        tp = 0
        fn = 0
        tn = 0
        fp = 0
        y_ans = []
        pred = []
        number += 1
        gc.enable()