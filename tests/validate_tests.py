import grader.utils as utils
from grader.autograder.tester import TestSuite

if __name__ == "__main__":
    lab_config = utils.load_json("config/labs/lab3.json")
    suite = TestSuite(lab_config["assignment"])
    print(suite.run_tests("./data/sollab5.py"))
