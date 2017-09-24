import json
from grader.submission.submission import Submission
from grader.group.group import GroupSubmission

def load_json(filename):
    fh = open(filename, "r")
    try:
        return json.load(fh)
    finally:
        fh.close()

def save_json(filename, data):
    fh = open(filename, "w")
    try:
        return json.dump(data, fh)
    finally:
        fh.close()

def convert_submission_dict_to_classes(submissions_dict):
    class_submissions = {}
    for student in submissions_dict:
        class_submissions[student] = Submission(submissions_dict[student])
    return class_submissions

def generate_group_submissions(submissions, groups):
    new_groups = {}
    for group_number in groups:
        group = GroupSubmission(group_number, groups, submissions)
        new_groups[group_number] = group
    return new_groups
