# -*- coding: utf-8 -*-

import tensorflow as tf
import random
import pickle
import json
from Helper import bow, handleInput
from training_conversation.Conversation import classify
from training_typequestion.TypeQuestions import typeQuestion
from training_characters.Characters import characters

# import intents file
with open('./training_conversation/conversation.json', encoding='utf-8') as json_data:
    intents = json.load(json_data)

# import type question file
with open('./training_typequestion/typequestion.json', encoding='utf-8') as json_data:
    type_question = json.load(json_data)

# import info characters file
with open('./training_infocharacters/infoCharacter.json', encoding='utf-8') as json_data:
    infocharacters = json.load(json_data)


def response(sentence):

    text = handleInput(sentence)

    results = classify(text)

    # print(results)
    # print(typeQuestion(text))
    # print(characters(text))

    if results:
        if results[0][0] == 'questions':
            # return '[Type] : ' + str(typeQuestion(text))
            while results:
                for i in infocharacters['info_characters']:
                    if(i['name'] == characters(text)[0][0]):
                        return i[typeQuestion(text)[0][0]]
        else:
            while results:
                for i in intents['intents']:
                    if i['tag'] == results[0][0]:
                        return random.choice(i['responses'])
