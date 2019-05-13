# -*- coding: utf-8 -*-

from underthesea import word_tokenize
import random
import tensorflow as tf
import tflearn
import numpy as np
import json


words = []
classes = []
documents = []
# stop_words = []

# f = open("stopwords.txt", mode="r", encoding="utf-8")
# for temp in f:
#     stop_words.append(temp.rstrip('\n'))
# f.close()

with open('characters.json', encoding='utf-8') as json_data_characters:
    intents = json.load(json_data_characters)

for intent in intents['characters']:
    for pattern in intent['patterns']:
        w = word_tokenize(pattern)

        words.extend(w)
        documents.append((w, intent['name']))
        if intent['name'] not in classes:
            classes.append(intent['name'])

words = [w.lower() for w in words]
words = sorted(list(set(words)))

classes = sorted(list(set(classes)))

# -----------------------------------------------
# create our training data
training = []
output = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [word.lower() for word in pattern_words]

    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)

# # create train and test lists
train_x = list(training[:,0])
train_y = list(training[:,1])

# #-----------------------------------------------
# # Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net, optimizer='adam', loss='categorical_crossentropy')

# # Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
# Start training
model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
model.save('model.tflearn')
# #-----------------------------------------------
import pickle
pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( "training_data", "wb" ) )
