from tester import TestSuite
from labChecker import PenalityLabGrader

class LabTester:
    def __init__(self, lab_config):
        self._test_suite = TestSuite(lab_config)
        self._penalty_test = PenalityLabGrader()

    def test_all_groups(self, groups):
        groups_grades = {}
        for group in groups:
            self.test_group(group)

    def test_group(self, group):
        group_grades = {}
        self._test_suite.run_tests(group.get_code())
        self._penalty_test.check_group(group)
