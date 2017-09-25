import grader.utils as utils
from grader.browser.gradeBrowser import GradeBrowser
from grader.interface.gradeHandler import GradeHandler
import code

def upload_grades(config, lab_number):
    # old params: grading_wb, usernames, groups, ta_username, ta_name, assignment_number
    groups = utils.load_json(config['groups json'])
    handler = GradeHandler(config['spreadsheet'], config['grader name'], groups, lab_number)
    browser = GradeBrowser(config)
    browser.upload_grades("Lab " + str(lab_number), handler)
    code.interact(local=locals())



if __name__ == "__main__":
    lab_number = 10
    config = utils.load_json("./config/general.json")
    upload_grades(config, lab_number)
