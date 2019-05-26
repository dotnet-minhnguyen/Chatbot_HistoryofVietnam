# -*- coding: utf-8 -*-

import tflearn
import tensorflow as tf
import pickle
import json
from Helper import bow
# ------------------ TYPE QUESTION ---------------------
data_typequestion = pickle.load(
    open("./training_typequestion/training_data", "rb"))
words_typequestion = data_typequestion['words']
classes_typequestion = data_typequestion['classes']
train_x_typequestion = data_typequestion['train_x']
train_y_typequestion = data_typequestion['train_y']

tf.reset_default_graph()
net_typequestion = tflearn.input_data(shape=[None, len(train_x_typequestion[0])])
net_typequestion = tflearn.fully_connected(net_typequestion, 8)
net_typequestion = tflearn.fully_connected(net_typequestion, 8)
net_typequestion = tflearn.fully_connected(
    net_typequestion, len(train_y_typequestion[0]), activation='softmax')
net_typequestion = tflearn.regression(net_typequestion, optimizer='adam',
                         loss='categorical_crossentropy')

model_typequestion = tflearn.DNN(
    net_typequestion, tensorboard_dir='./training_typequestion/tflearn_logs')
# ------------------ END TYPE QUESTION ---------------------

model_typequestion.load('./training_typequestion/model.tflearn')

ERROR_THRESHOLD_ = 0.5

def typeQuestion(sentence):
    results = model_typequestion.predict(
        [bow(sentence, words_typequestion)])[0]
    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD_]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes_typequestion[r[0]], r[1]))
    return return_list