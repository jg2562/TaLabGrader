from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from time import sleep
from lab import Lab, LabHandler
from requests import get
from os.path import exists, abspath
from os import makedirs
from shutil import rmtree
import comtypes.client

class GradeBrowser:
    def __init__(self):
        class_n = 'CS-126L'
        self._browser = Browser("chrome")
        self._browser.visit("http://bblearn.nau.edu")
        try:
            self._browser.find_by_xpath("//a[@id='CASButton']")[0].click()
        except ElementDoesNotExist:
            pass
        try:
            username = self._browser.find_by_xpath("//input[@id='username']")[0]
            if not username.value:
                username.type("jg2562")
        except ElementDoesNotExist:
            pass

        while self._browser.is_element_not_present_by_xpath("//a[contains(text(),'" + class_n + "')]"):
            sleep(1)
    
        self._browser.find_by_xpath("//a[contains(text(),'" + class_n + "')]").click()
        self._browser.find_by_xpath("//a[text()='Grade Center']").click()
        self._browser.find_by_xpath("//a[text()='Needs Grading']").click()
        self._browser.find_by_xpath("//a[@class='gradeAttempt']")[0].click()

    def convert_to_pdf(self, file):
        word = comtypes.client.CreateObject("Word.Application")
        doc = word.Documents.Open(file)
        nFile = file.split(".")
        nFile = nFile[0] + ".pdf"
        doc.SaveAs(file.split(), FileFormat=17)
        doc.Close()
        word.Quit()


    def get_documents(self, lab_name):
        dls = self._browser.find_by_xpath("//a[@class='dwnldBtn']")
        extens = {}
        files = []
        for dl in dls:
            req = get(dl["href"], cookies=self._browser.cookies.all())
            if not req.status_code == 200:
                print("Error downloading file")
            assignment = req.headers["Content-Disposition"].split(";")[1].split("=")[1][1:-1]
            exten = assignment.split('.')[1]

            if exten not in extens:
                extens[exten] = -1

            extens[exten] += 1

            mid = ""
            if exten == "py":
                mid = "code"
            elif exten in ["doc", "docx", "pdf"]:
                mid = "report"
            else:
                mid = "misc"

            directory = abspath("./" + mid + "/" + lab_name + "_" + str(extens[exten]) + "." + exten)

            fh = open(directory, 'wb')
            for chunk in req.iter_content(10000):
                fh.write(chunk)
            fh.close()
            if exten in ["doc", "docx"] and False:
                self.convert_to_pdf(directory)
                rmtree(directory)
                directory = directory.split(".")[0] + ".pdf"
            files.append(directory)
        return files

    def check_last_attempt(self):
        score = self._browser.find_by_xpath("//span[contains(text(),'(Attempt')]").value.split("Attempt")[1].split("of")
        return int(score[0]) == int(score[1].split(")")[0])

    def check_assignment(self, assignment):
        return self._browser.find_by_xpath("//span[@id = 'pageTitleText']").value.split(":")[1]\
                   .strip().lower() == assignment

    def get_person_name(self):
        return self._browser.find_by_xpath("//span[contains(text(),'(Attempt')]").value.split("(")[0].strip()

    def skip_assignment(self):
        self._browser.find_by_xpath("//a[@title='Grade Next Item']").click()

    def input_person_grade(self, grade, notes):
        grade_attempt = self._browser.find_by_xpath("//input[@id='currentAttempt_grade']")[0]
        grade_attempt.clear()
        grade_attempt.type(grade)

        sleep(0.75)
        comments = self._browser.find_by_xpath("//iframe[@id='feedbacktext_ifr']")[0]
        comments.clear()
        comments.type(notes)

        self._browser.find_by_xpath("//a[@id='currentAttempt_submitButton']")[0].click()

    def get_comment(self):
        return self._browser.find_by_xpath("//div[@class='vtbegenerated']")[0].value

    def apply_to_all_assignments(self, func):
        amount = int(self._browser.find_by_xpath("//span[@class='count']")
                     .value.split('of')[1].split('gradable')[0].strip())
        for i in range(amount):
            func()

    def enter_grades(self, assignment, grade_handler):

        def _enter_grade():
            if self.check_assignment(assignment):
                name = self.get_person_name()
                self.input_person_grade(grade_handler.get_grade(name), grade_handler.get_note(name))

            else:
                self.skip_assignment()

        self.apply_to_all_assignments(_enter_grade)

    def download_assignments(self, assignment, lab_handler):
        assignment = assignment.strip().lower()

        def _download():
            if self.check_assignment(assignment) and self.check_last_attempt():
                name = self.get_person_name()
                comment = self.get_comment()
                lab = Lab(name, comment=comment)
                files = self.get_documents(lab.get_lab_name())
                lab.add_files(files)
                lab_handler.add_lab(lab)
            self.skip_assignment()

        for dir in ['code', 'report', 'misc']:
            if exists("./" + dir):
                rmtree("./" + dir)
            makedirs("./" + dir)

        self.apply_to_all_assignments(_download)

    def close(self):
        self._browser.quit()

if __name__ == "__main__":
    lh = LabHandler()
    gb = GradeBrowser()
    gb.download_assignments("lab 12", lh)
    gb.close()