from grader import utils
from grader.autograder.labGrader import LabGrader

if __name__ == "__main__":
    config = utils.load_json("./config/general.json")
    lab_config = utils.load_json("./config/labs/lab3.json")
    submissions, groups = utils.generate_group_and_submissions_from_zip(config)
    grades = LabGrader(lab_config["assignment"]).get_group_grades(groups)
