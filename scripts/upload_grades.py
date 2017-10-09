import grader.utils as utils
from grader.browser.gradeBrowser import GradeBrowser
from grader.interface.gradeHandler import GradeHandler
from grader.interface.gradeSheet import GradeSheet

def upload_grades(config, lab_number):
    lab_config = utils.load_json("./config/labs/lab{}.json".format(lab_number))
    students = utils.load_json(config['submissions json'])
    groups = utils.load_json(config['groups json'])
    sheet_grades = GradeSheet(config).get_grades(lab_config)
    handler = GradeHandler(config, groups, students, lab_number, sheet_grades)
    browser = GradeBrowser(config)
    raise NotImplementedError
    browser.upload_grades("Lab " + str(lab_number), handler)
    print("Finished uploading grades")
    browser.close()

if __name__ == "__main__":
    lab_number = 4
    print("Uploading Lab {}.".format(lab_number))
    config = utils.load_json("./config/general.json")
    upload_grades(config, lab_number)
