import grader.utils as utils
from grader.autograder.cheatDetection import CheatDetector

if __name__ == "__main__":
    config = utils.load_json("config/general.json")
    submissions, groups = utils.generate_group_and_submissions_from_zip(config)
    cheatD = CheatDetector(config)._runMoss(groups, None)
