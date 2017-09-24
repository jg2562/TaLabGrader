import os
import os.path as path
from grader.utils import load_json
from time import sleep
from uuid import uuid1 as uuid
from requests import get
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import code

class GradeBrowser:
    def __init__(self, username, class_n):
        bblearn_url = "http://bblearn.nau.edu"
        self._browser = Browser("chrome")
        self._browser.visit(bblearn_url)
        self._login(username)

        while self._browser.is_element_not_present_by_xpath("//a[contains(text(),'" + class_n + "')]"):
            sleep(1)

        self._browser.find_by_xpath("//a[contains(text(),'" + class_n + "')]").click()
        self._course_id = self._get_course_id(self._browser.url)
        grade_center_url = bblearn_url + "/webapps/gradebook/do/instructor/enterGradeCetner?couse_id={}&cvid=fullGC"
        self._browser.visit(grade_center_url)

        # theGradeCenter.grid.model.colDefs has assignment ids

    def _login(self, username):
        try:
            self._browser.find_by_xpath("//a[@id='CASButton']")[0].click()
        except ElementDoesNotExist:
            pass

        try:
            username_input = self._browser.find_by_xpath("//input[@id='username']")[0]
            password_input = self._browser.find_by_xpath("//input[@id='password']")[0]
            if not username_input.value:
                username_input.type(username)
                password_input.type("")
        except ElementDoesNotExist:
            pass

    def _get_course_id(self, url):
        meta_info = url.split("?")[1].split("&")
        content_info = [meta_info_piece.split("=") for meta_info_piece in meta_info if "course_id" in meta_info_piece][0]
        return content_info[1]

    def get_attachments(self, assignment_dir):
        dls = self._browser.find_by_xpath("//a[@class='dwnldBtn']")
        files = []
        os.makedirs(assignment_dir)
        for dl in dls:
            req = get(dl["href"], cookies=self._browser.cookies.all())
            if not req.status_code == 200:
                print("Error downloading file")
            assignment = req.headers["Content-Disposition"].split(";")[1].split("=")[1][1:-1]
            file_extension = assignment.split('.')[1]

            new_assignment_name = uuid().hex + "." + file_extension
            directory = path.join(assignment_dir, new_assignment_name)
            directory = path.abspath(directory)

            fh = open(directory, 'wb')
            for chunk in req.iter_content(10000):
                fh.write(chunk)
            fh.close()

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
        try:
            return self._browser.find_by_xpath("//div[@class='vtbegenerated']")[0].value.strip()
        except ElementDoesNotExist:
            return ""

    def map_to_all_assignments(self, func, assignment_num):
        # cell_col_element = None
        # xpath_div_str = "//div[text()='Lab " + str(assignment_num) + "']"
        # if self._browser.is_element_present_by_xpath(xpath_div_str):
        #     cell_col_element = self._browser.find_by_xpath(xpath_div_str).find_by_xpath("../../..")
        # else:
        #     cell_num = 0
        #     while self._browser.is_element_present_by_xpath("//th[@id='cell_0_" + str(cell_num) + "']"):
        #         cell_num += 1
        #     cell_num -= 1
        #     last_text = ""

        # self._browser.find_by_xpath("//div[text()='Lab " + str(assignment_num) + "']")

        amount = int(self._browser.find_by_xpath("//span[@class='count']")
                     .value.split('of')[1].split('gradable')[0].strip())
        for i in range(amount):
            func()

    def enter_grades(self, assignment, grade_handler):

        def _enter_grade():
            if self.check_assignment(assignment):
                name = self.get_person_name()
                if grade_handler.contains_student(name):
                    self.input_person_grade(grade_handler.get_grade(name), grade_handler.get_note(name))
                else:
                    self.skip_assignment()
            else:
                self.skip_assignment()

        self.map_to_all_assignments(_enter_grade, assignment)

    def download_assignments(self, assignment, download_dir, user_ids):
        assignment = assignment.strip().lower()
        submissions = {}

        def _download():
            if self.check_assignment(assignment) and self.check_last_attempt():

                name = self.get_person_name()
                user_id = user_ids[name]
                comment = self.get_comment()
                submission_directory = path.join(download_dir, user_id)
                attachments = self.get_attachments(submission_directory)
                submission = {"username": user_id, "name": name, "comment": comment, "attachments": attachments}
                submissions[user_id] = submission
            self.skip_assignment()

        self.map_to_all_assignments(_download, assignment)
        return submissions

    def close(self):
        self._browser.quit()

if __name__ == "__main__":
    usernames = load_json("usernames.json")
    browser = GradeBrowser("jg2562")
    code.interact(local=locals())
