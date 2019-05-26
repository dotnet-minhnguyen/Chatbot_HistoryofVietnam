# -*- coding: utf-8 -*-

import tensorflow as tf
import random
import pickle
import json
from Helper import handleInput
from training_conversation.Conversation import classify
from training_typequestion.TypeQuestions import typeQuestion
from training_characters.Characters import characters
from underthesea import word_tokenize, pos_tag

# import intents file
with open('./training_conversation/conversation.json', encoding='utf-8') as json_data:
    intents = json.load(json_data)

# import type question file
with open('./training_typequestion/typequestion.json', encoding='utf-8') as json_data:
    type_question = json.load(json_data)

# import info characters file
with open('./data/infoCharacter.json', encoding='utf-8') as json_data:
    infocharacters = json.load(json_data)

# import characters file
with open('./training_characters/characters.json', encoding='utf-8') as json_data:
    characters_name = json.load(json_data)


def response(sentence):
    check = False
    text = handleInput(sentence)
    results = classify(text)

    # print(results)
    # print(typeQuestion(text))
    # print(characters(text))


    if results:
        if results[0][0] == 'questions':
            if(len(typeQuestion(text))>0):
                if(len(characters(text)) != 0):
                    for i in infocharacters['info_characters']:
                        if(i['name'] == characters(text)[0][0]):
                            return i[typeQuestion(text)[0][0]]

                # Lỗi tokenize nên phải có hàm này
                else:
                    for charac in characters_name["characters"]:
                        for name in charac["patterns"]:
                            if(text.find(str(name)) != -1):
                                for i in infocharacters['info_characters']:
                                    if(i["name"] == charac["name"]):
                                        return i[typeQuestion(text)[0][0]]
                                        check = True

                    if(check == False):
                        return "Tôi không hiểu câu hỏi :("
                check == False
            else:
                return "Tôi không hiểu câu hỏi :( , bạn thử nhập lại xem!"
        if(results[0][0] == 'greeting' or results[0][0] == 'goodbye' or results[0][0] == 'thanks'):
            for i in intents['intents']:
                if i['tag'] == results[0][0]:
                    return random.choice(i['responses'])
        else:
            return "Bạn viết thật khó để hiểu :/"
    else:
        return "Bạn viết thật khó để hiểu :/"
