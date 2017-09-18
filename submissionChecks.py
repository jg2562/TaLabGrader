import utils
import py_compile
from pycodestyle import StyleGuide


class GroupSubmissionGrader():
    def __init__(self):
        self.style_guide = StyleGuide(quiet=True)

    def check_groups(self, group_submissions):
        groups_errors = {}
        for group_number in group_submissions:
            group = group_submissions[group_number]
            code = group.get_code()
            if not code:
                group_errors = {"Pep8": None, "Syntax": None}
                groups_errors[group_number] = group_errors
                continue
            pep8 = self.check_pep8(code)
            syntax = self.check_syntax(code)
            group_errors = {"Pep8": pep8, "Syntax": syntax}
            groups_errors[group_number] = group_errors
        return groups_errors

    def check_group(self, group):
        code = group.get_code()
        if not code:
            pep8 = 0
            syntax = False
        else:
            pep8 = self.check_pep8(code)
            syntax = self.check_syntax(code)
        group_errors = {"Pep8": pep8, "Syntax": syntax}
        return group_errors

    def check_pep8(self, code_file):
        pep8_report = self.style_guide.check_files([code_file])
        return (pep8_report.get_file_results(), pep8_report.get_statistics())

    def check_syntax(self, code_file):
        try:
            py_compile.compile(code_file)
            return True
        except SyntaxError as e:
            return False


if __name__ == "__main__":
    groups = utils.load_json("groups.json")
    submissions = utils.load_json("students.json")
    submissions = utils.convert_submission_dict_to_classes(submissions)
    groups = utils.generate_group_submissions(submissions, groups)
    grader = GroupSubmissionGrader()
    grader.check_groups(groups)
