import json
import shutil
import argExtractor
import grader.utils as utils
from grader.group.partnerGrouper import PartnerGrouper
from grader.submission.submissionSorter import SubmissionSorter
from grader.interface.gradeSheet import GradeSheet
from grader.interface.commentGenerator import CommentGenerator
from grader.autograder.labGrader import LabGrader

def setup_assignment(config):
    submissions = SubmissionGenerator(config).generate_submissions()
    utils.save_json(config["submissions json"], submissions)
    return submissions

def students_to_sheet(config, submissions, lab_number):
    lab_config = utils.load_json("./config/labs/lab{}.json".format(lab_number))
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
    group_grades = LabGrader(lab_config).get_groups_grades(groups)

    CommentGenerator().add_comments_to_sheet(submissions, lab_number, lab_sheet_name)
    GradeSheet(config).create_grade_sheet(groups, lab_config, group_grades)

def setup_grades(config, lab_number):
    submissions = setup_assignment(config)
    students_to_sheet(config, submissions, lab_number)


if __name__ == "__main__":
    lab_number = argExtractor.get_lab_number()
    config = utils.load_json("./config/general.json")
    setup_grades(config, lab_number)
