import grader.utils as utils
from grader.autograder.tester import TestSuite


if __name__ == "__main__":
    config = utils.load_json("config/general.json")
    submissions, groups = utils.generate_group_and_submissions_from_zip(config)
    suite = TestSuite(config)
    runner = TestRunner(config, "../data/tests/fakelab/col1.py")
