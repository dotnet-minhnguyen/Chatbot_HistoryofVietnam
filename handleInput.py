# -*- coding: utf-8 -*-

import tensorflow as tf
import random
import pickle
import json
import re

from Helper import handleInput
from training_conversation.Conversation import classify
from training_typequestion_characters.TypeQuestions import typeQuestion
from training_characters.Characters import characters
from GetApi import getLinkGoogle, getLinkWiki
from training_typequestion_events.TypeEventQuestions import typeEventQuestion
from training_events.Events import events

# import intents file
with open('./training_conversation/conversation.json', encoding='utf-8') as json_data:
    intents = json.load(json_data)

# import type question file
with open('./training_typequestion_characters/typequestion.json', encoding='utf-8') as json_data:
    type_question = json.load(json_data)



# import data characters file
with open('./data/infoCharacter.json', encoding='utf-8') as json_data:
    infocharacters = json.load(json_data)

# import data event file
with open('./data/historic_events.json', encoding='utf-8') as json_data:
    infoevent = json.load(json_data)

# import answer question file
with open('./training_typequestion_characters/answerquestion.json', encoding='utf-8') as json_data:
    answer_question = json.load(json_data)

# import characters file
with open('./training_characters/characters.json', encoding='utf-8') as json_data:
    characters_name = json.load(json_data)


def response(sentence):
    text = handleInput(sentence)

    # print(text)
    # print(classify(text))
    # print(typeQuestion(text))
    # print(characters(text))
    # print(typeEventQuestion(text))
    # print(events(text))
    
    # chuỗi search theo goole or wiki
    if text.find("google") != -1 or text.find("wiki") != -1:

        if(text.find("google") != -1):

            text = text.replace('google', '')
            text = handleInput(text)
            text = text.replace(' ', '%20')
            return getLinkGoogle(text)

        if(text.find("wiki") != -1):

            text = text.replace('wiki', '')
            text = handleInput(text)
            text = text.replace(' ', '%')

            return getLinkWiki(text)
    
    # chuỗi bt
    else:
        # tách chuỗi
        sentences = re.split(',|-| và ', text)
        results = classify(text)
        if results:
            char_name = ''

            # loại câu search theo tên In hoa có dấu
            if results[0][0] == "characters":
                for charac in characters_name["characters"]:
                    for name in charac["patterns"]:
                        if(text.find(str(name)) != -1):
                            for i in infocharacters['info_characters']:
                                if(i["name"] == charac["name"]):
                                    return i["brief"]

            # loại câu giao tiếp
            if(results[0][0] == 'greeting' or results[0][0] == 'goodbye' or results[0][0] == 'thanks'):
                for i in intents['intents']:
                    if i['tag'] == results[0][0]:
                        return random.choice(i['responses'])

            # loại câu hỏi
            if results[0][0] == 'questions':

                # xác định nhân vật
                for item in sentences:
                    if(len(characters(item)) == 0):
                        for charac in characters_name["characters"]:
                            for name in charac["patterns"]:
                                if(item.find(str(name)) != -1):
                                    char_name = charac["name"]
                    else:
                        char_name = characters(item)[0][0]

                # chưa có dữ liệu nhân vật
                if char_name == "":
                    return "Chưa có dữ liệu :("
                else :
                    array_sentences = []

                    # ghép chuỗi với tên nhân vật vừa tách
                    if len(sentences) > 1:
                        for item in sentences:
                            if(item.find(char_name) == -1):
                                array_sentences.append(handleInput(item + " của " + char_name))
                            else:
                                array_sentences.append(handleInput(item))
                    else:
                        array_sentences = sentences

                    # đưa các câu trả lời vào list
                    array_answer = []
                    for x in array_sentences:
                        for y in answer_question["answerquestion"]:
                            if y["type"] == typeQuestion(x)[0][0]:
                                if Result(x) == "-1":
                                    array_answer.append(Result(x))
                                else:
                                    array_answer.append(y["patterns"][0] + Result(x))

                    # xuất câu trả lời
                    ans = ''
                    for x in array_answer:
                        if x == array_answer[-1]:
                            if x == "-1":
                                ans = ans + "(chưa có dữ liệu)"
                            else:
                                ans = ans + x
                        else:
                            if x == "-1":
                                ans = ans + "(chưa có dữ liệu)" + " - "
                            else:
                                ans = ans + x + " - "

                    return ans

            temp = 0
            if results[0][0] == "event":
                text = text.lower()
                print(text)
                for name_event in infoevent['historic_event']:
                    if (events(text) != []):
                        if name_event['name'] == events(text)[0][0]:
                            if typeEventQuestion(text) != []:
                                return name_event[typeEventQuestion(text)[0][0]]
                                # print (typeEventQuestion(text))
                                # print (events(text))
                            else:
                                temp +=1
                    else:
                        temp +=1
                if(temp != 0 ):
                    return "Chưa có dữ liệu :<"
                    temp = 0
        else:
            return "Bạn viết thật khó để hiểu :/"


def Result(text):
    if(len(typeQuestion(text)) > 0):
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
