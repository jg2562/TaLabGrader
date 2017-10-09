import argExtractor
import grader.utils as utils
from grader.browser.gradeBrowser import GradeBrowser
from setup_grades import setup_grades

def download_assignments(config, lab_number):
    browser = GradeBrowser(config)
    students = browser.download_assignments("Lab " + str(lab_number))

    print("Finished downloading assignments")
    setup_grades(config, lab_number)
    browser.close()

if __name__ == "__main__":
    lab_number = argExtractor.get_lab_number()
    print("Downloading Lab {}.".format(lab_number))
    config = utils.load_json("./config/general.json")
    download_assignments(config, lab_number)
