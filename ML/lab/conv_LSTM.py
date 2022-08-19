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
num_classes = 2

def mcc(tp,tn,fp,fn):
    mcc_out = ((tp*tn)-(fp*fn))/math.sqrt((tp+fn)*(fp+tn)*(tp+fp)*(fn+tn))
    mcc_out = round(mcc_out,4)
    return mcc_out
def sp(tn,fp):
    sp_out = tn/(fp+tn)
    sp_out = round(sp_out,4)
    return sp_out
def sn(tp,fn):
    sn_out = tp/(tp+fn)
    sn_out = round(sn_out,4)
    return sn_out
def f1(tp,fn,fp):
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
#	print('Usage: {0} training_result_file [training_feature_file] [testing_result_file] [testing_feature_file]'.format(sys.argv[0]))
#	raise SystemExit
#
#train_result_pathname = sys.argv[1]
#train_feature_pathname = sys.argv[2]
#assert os.path.exists(train_result_pathname),"training result file not found"
#assert os.path.exists(train_feature_pathname),"training feature file not found"
#file_name = os.path.split(train_result_pathname)[1]
#
#if len(sys.argv) > 4:
#	test_result_pathname = sys.argv[3]
#	file_name

MHC_ml_read = open('C:\\Users\\allen\\Desktop\\Esther\\number_allele_specific_ml.txt','r')
MHC_dl_read = open('C:\\Users\\allen\\Desktop\\Esther\\number_allele_specific_dl.txt','r')

MHC_ml = []
MHC_dl = []
for j in MHC_ml_read:
	jj = j.split('\t')
	MHC_ml.append(jj[0])
	MHC_ml.append('0')
#    gc.collect()
for j in MHC_dl_read:
	jj = j.split('\t')
	MHC_dl.append(jj[0])
	MHC_dl.append('0')
#    gc.collect()

MHC_ml_read.close()
MHC_dl_read.close()

path="C:\\Users\\allen\\Desktop\\Esther\\dl\\conv_LSTM\\";
model_path="C:\\Users\\allen\\Desktop\\Esther\\dl\\conv_LSTM\\model\\";
trian_path="C:\\Users\\allen\\Desktop\\Esther\\dl\\Training\\all\\mlp\\";
test_path="C:\\Users\\allen\\Desktop\\Esther\\dl\\Testing\\mlp\\";


filep=open(path+'dl_conv_LSTM_result.txt',"a")

trian_files = listdir(trian_path)
test_files = listdir(test_path)
y_ans = []
pred = []
tp = 0
tn = 0
fp = 0
fn = 0
filep.write('MHC\tloss\tacc\tauc\tmcc\tf1\tsp\tsn\ttp\tfn\ttn\tfp\n')
for t in range(0,len(MHC_dl),2):
    print(t)
    print(trian_path+trian_files[t])
    x = np.loadtxt(open(trian_path+trian_files[t+1], "rb"), delimiter=",")
    x = np.expand_dims(x, axis=2)
    print(x.shape)

    y = np.loadtxt(open(trian_path+trian_files[t], "rb"), delimiter=",")
#    y = np.expand_dims(y, axis=2)
    print(y.shape)

    test_x = np.loadtxt(open(test_path+test_files[t+1], "rb"), delimiter=",")
    test_x = np.expand_dims(test_x, axis=2)
    print(test_x.shape)
    test_x2 = np.loadtxt(open(test_path+test_files[t], "rb"), delimiter=",")
#    test_x2 = np.expand_dims(test_x2, axis=2)
    print(test_x2.shape)     

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv1D(32, 3, activation='elu', input_shape=(x.shape[1], 1)))
    model.add(tf.keras.layers.MaxPooling1D(2))
    model.add(tf.keras.layers.Conv1D(32, 5, activation='elu'))
    model.add(tf.keras.layers.MaxPooling1D(2))
    model.add(tf.keras.layers.Conv1D(16, 5, activation='elu'))
    model.add(tf.keras.layers.MaxPooling1D(4))
    #model.add(tf.keras.layers.Flatten())
    #model.add(tf.keras.layers.GlobalAveragePooling1D())
    model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(units=40, activation='tanh', recurrent_activation='hard_sigmoid', use_bias=True, kernel_initializer='glorot_uniform', recurrent_initializer='orthogonal', bias_initializer='zeros', unit_forget_bias=True, kernel_regularizer=None, recurrent_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, recurrent_constraint=None, bias_constraint=None, dropout=0.0, recurrent_dropout=0.0, implementation=1, return_sequences=False, return_state=False, go_backwards=False, stateful=False, unroll=False)))
    #model.add(tf.keras.layers.SimpleRNN(units=40, activation='tanh', use_bias=True, kernel_initializer='glorot_uniform', recurrent_initializer='orthogonal', bias_initializer='zeros', kernel_regularizer=None, recurrent_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, recurrent_constraint=None, bias_constraint=None, dropout=0.0, recurrent_dropout=0.0, return_sequences=False, return_state=False, go_backwards=False, stateful=False, unroll=False))
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.Dense(num_classes, activation='softmax'))

    model.compile(loss=tf.keras.losses.categorical_crossentropy,
                  #optimizer=tf.keras.optimizers.Adadelta(lr=0.01, clipnorm=1.),
                  #optimizer=tf.keras.optimizers.Adagrad(lr=0.01, clipnorm=1.),
                  optimizer=tf.keras.optimizers.Adam(lr=0.0001, clipnorm=1.),
                  #optimizer=tf.keras.optimizers.Adamax(lr=0.01, clipnorm=1.),
                  #optimizer=tf.keras.optimizers.Nadam(lr=0.01, clipnorm=1.),             
                  #optimizer=tf.keras.optimizers.RMSprop(lr=0.01, clipnorm=1.),
                  #optimizer=tf.keras.optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True),
                  metrics=['accuracy'])
                  #metrics=[tf.keras.metrics.categorical_accuracy])
    my_callbacks = [EarlyStopping(monitor='val_loss', patience=10, verbose=1, mode='min')]

# class_weight = {0: 3.,
#                 1: 3.,
#               }
    model.fit(x, y,
#    validation_split=0.3,
#    shuffle=True,
    batch_size=10,
    epochs=1000,
    verbose=1,
    #class_weight=class_weight,
    validation_data=(test_x, test_x2),
    callbacks=my_callbacks)
    file_name = MHC_dl[t].replace(':','_')
    file_name = file_name.replace('*','_')
    print(file_name)
    file_save = model_path+file_name+'_mlp.h5'
    model.save(file_save)
##		model2 = tf.contrib.keras.models.load_model('my_model.h5')
    results = model.predict(test_x,verbose=0)
    resultsClass2 = model.predict_classes(test_x,verbose=0)
    for num in range(0,len(resultsClass2)):
        if test_x2[num][0] == 1.0 and test_x2[num][1] == 0.0 and resultsClass2[num] == 0:
            tn += 1
            y_ans.append(0)
            pred.append(0)
        elif test_x2[num][0] == 1.0 and test_x2[num][1] == 0.0 and resultsClass2[num] == 1:
            fn += 1
            y_ans.append(1)
            pred.append(0)
        elif test_x2[num][0] == 0.0 and test_x2[num][1] == 1.0 and resultsClass2[num] == 1:
            tp += 1
            y_ans.append(1)
            pred.append(1)
        elif test_x2[num][0] == 0.0 and test_x2[num][1] == 1.0 and resultsClass2[num] == 0:
            fp += 1
            y_ans.append(0)
            pred.append(1)
    score = model.evaluate(test_x, test_x2, verbose=0)
    filep.write(MHC_dl[t]+"\t")
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
    
filep.close()