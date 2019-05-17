# -*- coding: utf-8 -*-

import tflearn
import tensorflow as tf
import pickle
import json
from cleanupSentence import bow

# # ------------------ CONVERSATION ---------------------
data_conversation = pickle.load(
    open("./training_conversation/training_data", "rb"))
words_conversation = data_conversation['words']
classes_conversation = data_conversation['classes']
train_x_conversation = data_conversation['train_x']
train_y_conversation = data_conversation['train_y']

tf.reset_default_graph()
net_conversation = tflearn.input_data(shape=[None, len(train_x_conversation[0])])
net_conversation = tflearn.fully_connected(net_conversation, 8)
net_conversation = tflearn.fully_connected(net_conversation, 8)
net_conversation = tflearn.fully_connected(
    net_conversation, len(train_y_conversation[0]), activation='softmax')
net_conversation = tflearn.regression(net_conversation, optimizer='adam',
                         loss='categorical_crossentropy')

model_conversation = tflearn.DNN(
    net_conversation, tensorboard_dir='./training_conversation/tflearn_logs')
# ------------------ END CONVERSATION ---------------------

model_conversation.load('./training_conversation/model.tflearn')

ERROR_THRESHOLD = 0.25

def classify(sentence):
    results = model_conversation.predict(
        [bow(sentence, words_conversation)])[0]
    results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes_conversation[r[0]], r[1]))
    return return_list
