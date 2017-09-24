import json
import grader.utils as utils
from grader.submission.submissionGenerator import SubmissionGenerator


if __name__ == "__main__":
    config = utils.load_json("config/general.json")
    utils.save_json(config["submissions json"], SubmissionGenerator(config).generate_submissions())
