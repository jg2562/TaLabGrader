import utils
from gradeHandler import GradeHandler
from gradeBrowser import GradeBrowser

def upload_grades(grading_wb, usernames, groups, ta_username, ta_name, assignment_number):
    handler = GradeHandler(grading_wb, "Jack", groups, usernames, assignment_number)
    browser = GradeBrowser(ta_username)
    browser.enter_grades("lab " + str(assignment_number), handler)


if __name__ == "__main__":
    usernames = utils.load_json("usernames.json")
    groups = utils.load_json("groups.json")
    upload_grades("./grade-sheet.xlsx", usernames, groups, "jg2562", "Jack", 1)
