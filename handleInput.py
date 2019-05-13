# -*- coding: utf-8 -*-

import tflearn
import tensorflow as tf
import random
import pickle
import json
from cleanupSentence import bow
from training_conversation.Conversation import classify
from training_typequestion.TypeQuestions import typeQuestion
from training_characters.Characters import characters

# import intents file
with open('./training_conversation/conversation.json', encoding='utf-8') as json_data:
    intents = json.load(json_data)

# import type question file
with open('./training_typequestion/typequestion.json', encoding='utf-8') as json_data:
    type_question = json.load(json_data)
    
def response(sentence):
    results = classify(sentence)
    print(results)
    if results:
        if results[0][0] == 'questions':
            print(typeQuestion(sentence))
            print(characters(sentence))
        else:
            while results:
                for i in intents['intents']:
                    if i['tag'] == results[0][0]:
                        return random.choice(i['responses'])
