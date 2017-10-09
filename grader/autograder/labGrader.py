from grader.autograder.tester import TestSuite

class LabGrader():
    def __init__(self, lab_config):
        self._config = lab_config
        self._suite = TestSuite(lab_config)

    def get_groups_grades(self, groups):
        grades = {}
        for group in groups:
            grades[group] = self._suite.run_tests(groups[group].get_code())
        return grades
