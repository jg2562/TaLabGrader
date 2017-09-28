import grader.utils as utils
from grader.autograder.cheatDetection import CheatDetector

if __name__ == "__main__":
    config = utils.load_json("config/general.json")
    submissions, groups = utils.generate_group_and_submissions_from_zip(config)
    cheatD = CheatDetector(config)
    # url = cheatD._run_moss(groups, None)
    url = "http://moss.stanford.edu/results/84176306"
    ratings = cheatD._get_cheat_map_from_url(url, 70, 100)
    print(ratings)
