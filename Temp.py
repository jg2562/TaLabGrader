import textract
import os
from gradeHandler import GradeHandler

gh = GradeHandler()

partners = {}

for path in os.listdir("./report"):
    file = os.path.abspath("./report/" + path)
    if file.split(".")[1] == "pdf":
        try:
            test = ""
            text = textract.process(file).decode().lower().replace(" ","")
            print("======{}======".format(path))
            print(text)
            partners[path] = set([stu for stu in gh.get_all_students() if text.find("".join(stu.split(" ")[1:]).lower()) != -1])
        except UnicodeDecodeError as e:
            pass
print("============================")
for student in partners:
    print("student: {}\t partners: {}".format(student, partners[student]))
