# -*- coding: utf-8 -*-

import tflearn
import tensorflow as tf
import pickle
import json
from cleanupSentence import bow
# ------------------ TYPE QUESTION ---------------------
data_characters = pickle.load(
    open("./training_characters/training_data", "rb"))
words_characters = data_characters['words']
classes_characters = data_characters['classes']
train_x_characters = data_characters['train_x']
train_y_characters = data_characters['train_y']

tf.reset_default_graph()
net_characters = tflearn.input_data(shape=[None, len(train_x_characters[0])])
net_characters = tflearn.fully_connected(net_characters, 8)
net_characters = tflearn.fully_connected(net_characters, 8)
net_characters = tflearn.fully_connected(
    net_characters, len(train_y_characters[0]), activation='softmax')
net_characters = tflearn.regression(net_characters, optimizer='adam',
                         loss='categorical_crossentropy')

model_characters = tflearn.DNN(
    net_characters, tensorboard_dir='./training_characters/tflearn_logs')
# ------------------ END TYPE QUESTION ---------------------

model_characters.load('./training_characters/model.tflearn')

ERROR_THRESHOLD_ = 0.25

def characters(sentence):
    results = model_characters.predict(
        [bow(sentence, words_characters)])[0]
    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD_]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes_characters[r[0]], r[1]))
    return return_list