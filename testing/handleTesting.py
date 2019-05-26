# -*- coding: utf-8 -*-

import json

with open('../training_characters/characters.json', encoding='utf-8') as json_data:
    characters = json.load(json_data)

with open('../training_typequestion/typequestion.json', encoding='utf-8') as json_data:
    questions = json.load(json_data)


def partternQuestions():
    characters_array = []
    questions_array = []
    partterns_array = []

    for character in characters["characters"]:
        for name in character["patterns"]:
            characters_array.append(name)

    for question in questions["typequestion"]:
        for pattern in question["patterns"]:
            questions_array.append(pattern)

    for character in characters_array:
        for question in questions_array:
            partterns_array.append(character + ' ' + question)

    return partterns_array