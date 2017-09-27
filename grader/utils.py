import json
from grader.submission.submission import Submission
from grader.submission.submissionGenerator import SubmissionGenerator
from grader.group.group import GroupSubmission
from grader.group.partnerGrouper import PartnerGrouper

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
    class_submissions = {k: Submission(submissions_dict[k]) for k in submissions_dict}
    return class_submissions

def generate_group_submissions(submissions, groups):
    new_groups = {}
    for group_number in groups:
        group = GroupSubmission(group_number, groups, submissions)
        new_groups[group_number] = group
    return new_groups

def generate_group_and_submissions_from_json(config):
    submissions = convert_submission_dict_to_classes(load_json(config['submissions json']))
    groups = generate_group_submissions(submissions, load_json(config['groups json']))
    return (submissions, groups)

def generate_group_and_submissions_from_zip(config):
    submissions = convert_submission_dict_to_classes(SubmissionGenerator(config).generate_submissions())
    groups = generate_group_submissions(submissions, PartnerGrouper(submissions).generate_groups())
    return (submissions, groups)
