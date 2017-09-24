import json
import shutil
import grader.utils as utils
from grader.group.partnerGrouper import PartnerGrouper
from grader.submission.submissionSorter import SubmissionSorter
from grader.interface.gradeSheet import GradeSheet
from grader.submission.submissionChecks import GroupSubmissionGrader
from grader.interface.commentGenerator import CommentGenerator
from grader.submission.submissionGenerator import SubmissionGenerator

def setup_assignment(config):
    return SubmissionGenerator(config).generate_submissions()

def students_to_sheet(config, submissions, lab_number):
    lab_sheet_name = config["spreadsheet"]
    rubric_name = config["rubric"]
    groups_dir = config["groups dir"]
    groups_json = config["groups json"]
    submissions = utils.convert_submission_dict_to_classes(submissions)
    groups = PartnerGrouper(submissions).generate_groups()
    utils.save_json(groups_json, groups)
    shutil.rmtree(groups_dir, ignore_errors=True)
    SubmissionSorter(submissions, groups).create_group_submissions(groups_dir)
    groups = utils.generate_group_submissions(submissions, groups)
    CommentGenerator().add_comments_to_sheet(submissions, lab_number, lab_sheet_name)
    GradeSheet(lab_sheet_name).create_grade_sheet(groups, rubric_name, lab_number)

def setup_grades(config, lab_number):
    submissions = setup_assignment(config)
    students_to_sheet(config, submissions, lab_number)


if __name__ == "__main__":
    lab_number = 10
    config = utils.load_json("./config/general.json")
    setup_grades(config, lab_number)
