import grader.utils as utils
from grader.browser.gradeBrowser import GradeBrowser
from grader.interface.gradeHandler import GradeHandler

def upload_grades(config, lab_number):
    groups = utils.load_json(config['groups json'])
    handler = GradeHandler(config, groups, lab_number)
    browser = GradeBrowser(config)
    browser.upload_grades("Lab " + str(lab_number), handler)

    print("Finished uploading grades")

if __name__ == "__main__":
    lab_number = 10
    print("Uploading Lab {}.".format(lab_number))
    config = utils.load_json("./config/general.json")
    upload_grades(config, lab_number)
