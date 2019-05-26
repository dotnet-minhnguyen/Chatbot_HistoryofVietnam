from handleTesting import partternQuestions
import codecs

file = codecs.open("question_test.txt", "wb", "utf-8")
for question in partternQuestions():
    file.write(question + "\n")
file.close()

