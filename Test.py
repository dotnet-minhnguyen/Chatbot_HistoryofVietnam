# -*- coding: utf-8 -*-

import json
import codecs
from training_typequestion.TypeQuestions import typeQuestion
from training_characters.Characters import characters

with open('./training_characters/characters.json', encoding='utf-8') as json_data:
    characters_array = json.load(json_data)

with open('./training_typequestion/typequestion.json', encoding='utf-8') as json_data:
    questions_array = json.load(json_data)

# import characters file
with open('./training_characters/characters.json', encoding='utf-8') as json_data:
    characters_name = json.load(json_data)

total_true = 0
total_false = 0
pattern_true = 0
pattern_false = 0
total_pattern_true = 0
total_pattern_false = 0
array = []
file = codecs.open("result.txt", "wb", "utf-8")

for character in characters_array["characters"]:
    name_character = character["name"]
    file.write(
        "## {0}\t\n--------------------------\n\n".format(name_character))
    for name in character["patterns"]:
        for question in questions_array["typequestion"]:
            type_quest = question["type"]
            for pattern in question["patterns"]:
                text = str(name + ' ' + pattern)

                if(len(characters(text)) != 0):
                    if(str(characters(text)).find(name_character) != -1 and str(typeQuestion(text)).find(type_quest) != -1):
                        pattern_true += 1
                        total_pattern_true += 1
                        total_true += 1
                        file.write("True\t{0}\t{1}\t{2}\t{3}\t{4}\n".format(
                            name_character, type_quest, characters(text), typeQuestion(text), text))
                    else:
                        pattern_false += 1
                        total_pattern_false += 1
                        total_false += 1
                        file.write("False\t{0}\t{1}\t{2}\t{3}\t{4}\n".format(
                            name_character, type_quest, characters(text), typeQuestion(text), text))
                else:
                    for charac in characters_name["characters"]:
                        for name in charac["patterns"]:
                            if(text.find(str(name)) != -1 and str(typeQuestion(text)).find(type_quest) != -1):
                                pattern_true += 1
                                total_pattern_true += 1
                                total_true += 1
                                file.write("True\t{0}\t{1}\t{2}\t{3}\t{4}\n".format(
                                    name_character, type_quest, characters(text), typeQuestion(text), text))
                                break

                            else:
                                pattern_false += 1
                                total_pattern_false += 1
                                total_false += 1
                                file.write("False\t{0}\t{1}\t{2}\t{3}\t{4}\n".format(
                                    name_character, type_quest, characters(text), typeQuestion(text), text))
                                break
                        break

            file.write("\n\n{0}: total: {1}\ttrue: {2}\tfalse: {3}\trate: {4}\n\n-----\n".format(
                type_quest, pattern_true + pattern_false, pattern_true, pattern_false, pattern_true/(pattern_true + pattern_false)))

            pattern_true = 0
            pattern_false = 0

    file.write("""###############\nTOTAL: total: {1}\ttrue: {2}\tfalse: {3}\trate: {4}\n
                \n#######################################################################
                \n\n""".format(type_quest, (total_pattern_true + total_pattern_false), total_pattern_true, total_pattern_false, (total_pattern_true/(total_pattern_false + total_pattern_true))))
    total_pattern_true = 0
    total_pattern_false = 0

file.write("""\n===============\n
            TOTAL: total: {0}\ttrue: {1}\tfalse: {2}\trate: {3}""".format((total_true+total_false), total_true, total_false, (total_true/(total_false + total_true))))

file.close()
