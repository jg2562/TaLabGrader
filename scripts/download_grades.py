import json
import shutil
import grader.utils as utils
from grader.group.partnerGrouper import PartnerGrouper
from grader.submission.submissionSorter import SubmissionSorter
from grader.interface.gradeSheet import GradeSheet
from grader.browser.gradeBrowser import GradeBrowser
from grader.submission.submissionChecks import GroupSubmissionGrader
from grader.interface.commentGenerator import CommentGenerator

def get_assignments(student_usernames_file, ta_username, lab_number, download_dir):
    shutil.rmtree(download_dir, ignore_errors=True)
    usernames = utils.load_json(student_usernames_file)
    browser = GradeBrowser(ta_username)
    students = browser.download_assignments("lab " + str(lab_number), download_dir, usernames)
    utils.save_json("students.json", students)
    browser.close()
    return students

def students_to_sheet(submissions, lab_sheet_name, rubric_name, groups_dir, lab_number):
    submissions = utils.convert_submission_dict_to_classes(submissions)
    groups = PartnerGrouper(submissions).generate_groups()
    utils.save_json("groups.json", groups)
    shutil.rmtree(groups_dir, ignore_errors=True)
    SubmissionSorter(submissions, groups).create_group_submissions(groups_dir)
    groups = utils.generate_group_submissions(submissions, groups)
    CommentGenerator().add_comments_to_sheet(submissions, lab_number, lab_sheet_name)
    GradeSheet(lab_sheet_name).create_grade_sheet(groups, rubric_name, lab_number)

if __name__ == "__main__":
    # submissions = get_assignments("usernames.json", "jg2562", 1, "data")
    submissions = utils.load_json("students.json")
    students_to_sheet(submissions, "grade-sheet.xlsx", "grade-sheet.xlsx", "./groups/", 1)

