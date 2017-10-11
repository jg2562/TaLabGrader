import os
import os.path as path
from grader.utils import load_json
from time import sleep
from uuid import uuid1 as uuid
from requests import get
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from selenium.common.exceptions import WebDriverException
import code

class GradeBrowser:
    def __init__(self, config):
        bblearn_url = config["bblearn url"]
        self._config = config
        self._browser = Browser("chrome")
        self._browser.visit(bblearn_url)
        self._login()

        while self._browser.is_element_not_present_by_xpath("//a[contains(text(),'" + config["class name"] + "')]"):
            sleep(1)

        self._browser.find_by_xpath("//a[contains(text(),'" + config["class name"] + "')]").click()
        self._course_id = self._get_course_id(self._browser.url)
        grade_center_url = bblearn_url +\
        "/webapps/gradebook/do/instructor/enterGradeCenter?course_id={}&cvid=fullGC".format(self._course_id)
        self._browser.visit(grade_center_url)

        # Delay until grade center has populated
        while self._browser.evaluate_script("theGradeCenter.grid.model.getColDefs(true, true).length") == 0:
            sleep(0.1)


    def _login(self):
        try:
            self._browser.find_by_xpath("//a[@id='CASButton']")[0].click()
        except ElementDoesNotExist:
            pass

        try:
            username = self._config["grader username"]
            password = ""
            if 'grader password' in self._config:
                password = self._config["grader password"]
            username_input = self._browser.find_by_xpath("//input[@id='username']")[0]
            password_input = self._browser.find_by_xpath("//input[@id='password']")[0]
            if not username_input.value:
                username_input.type(username)
            if not password_input.value:
                password_input.type(password)
            if password:
                self._browser.find_by_xpath("//input[@type='submit']")[0].click()
        except ElementDoesNotExist:
            pass

    def _get_course_id(self, url):
        meta_info = url.split("?")[1].split("&")
        content_info = [meta_info_piece.split("=") for meta_info_piece in meta_info if "course_id" in meta_info_piece][0]
        return content_info[1]

    def download_assignments(self, assignment):
        assignment_id = self._get_assignment_id(assignment)
        self._browser.visit("https://bblearn.nau.edu/webapps/gradebook/do/instructor/" +
                            "downloadAssignment?outcome_definition_id={itemId}&course_id={courseId}&showAll=true".format(
                                itemId=assignment_id, courseId=self._course_id))
        self._browser.find_by_xpath("//input[@id='listContainer_selectAll']").check()
        self._browser.find_by_xpath("//input[@id='lastAttemptFile']").check()
        self._browser.find_by_xpath("//input[@type='submit']").click()
        self._download_submissions_zip(self._config['zip file'])

    def _get_assignment_id(self, assignment):
        try:
            return self._browser.evaluate_script("theGradeCenter.grid.model.getColDefs(true, true).find(function(element){{return element['name'] == '{assignment}';}})['id']".format(assignment=assignment))
        except WebDriverException:
            raise ValueError("Assignment '{}' does not exist.".format(assignment))

    def _download_submissions_zip(self, zip_file):
        dl = self._browser.find_by_xpath("//a[contains(text(),'assignment')]")[0]
        req = get(dl["href"], cookies=self._browser.cookies.all())
        if not req.status_code == 200:
            print("Error downloading file")
        directory = path.abspath(zip_file)

        fh = open(directory, 'wb')
        for chunk in req.iter_content(10000):
            fh.write(chunk)
        fh.close()

    def get_user_data(self):
        # TODO separate scripts into a script dictionary called by browser_do function, parameters could be para**
        raw_user_data = self._browser.evaluate_script("theGradeCenter.grid.model.rows.map(function(x){return [x[0].v, x[1].v, x[2].v, x[3].v]})")
        return raw_user_data

    def _get_user_id_map(self):
        userIdMap = {x[0]:x[1] for x in self._browser.evaluate_script("theGradeCenter.grid.model.rows.map(function(x){return [x[2].v, x[0].uid]})")}
        return userIdMap

    def upload_grades(self, assignment, grades):
        colId = self._get_assignment_id(assignment)
        userIdMap = self._get_user_id_map()
        for user in userIdMap:
            if grades.contains_student(user):
                script = "theGradeCenter.grid.model.getColDefById({}).updateGrade('{}', {})".format(colId, grades.get_grade(user), userIdMap[user])
                # TODO: Use proper delay based on website
                sleep(0.5)
                self._browser.evaluate_script(script)
                script = "theGradeCenter.grid.model.setComments({},{},'{}','')".format(userIdMap[user], colId, grades.get_comment(user).replace("\n", "<br>"))
                sleep(0.5)
                self._browser.evaluate_script(script)

    def _scroll_to_assignment(self, assignment_id):
        self._browser.execute_script("theGradeCenter.grid.scrollGradeItemIntoViewPort({});".format(assignment_id))

    def close(self):
        # Here until I can figure out how to kill browser
        raise NotImplementedError("Preventing browser hang")
        self._browser.quit()
