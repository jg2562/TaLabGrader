import grader.utils as utils
import py_compile
from pycodestyle import StyleGuide


class GroupSubmissionGrader():
    def __init__(self):
        self.style_guide = StyleGuide(quiet=True)

    def check_groups(self, group_submissions):
        groups_errors = {}
        for group_number in group_submissions:
            group = group_submissions[group_number]
            groups_errors[group_number] = self.check_group(group)
        return groups_errors

    def check_group(self, group):
        code = group.get_code()
        if not code:
            pep8 = (0, "")
            syntax = False
        else:
            pep8 = self.check_pep8(code)
            syntax = self.check_syntax(code)
        group_errors = {"pep8": pep8, "syntax": syntax}
        return group_errors

    def check_pep8(self, code_file):
        result = (0, [])
        if code_file:
            pep8_report = self.style_guide.check_files([code_file])
            result = (int(pep8_report.get_file_results()), pep8_report.get_statistics())
        return (result[0], "\n".join(result[1]))

    def check_syntax(self, code_file):
        result = False
        if code_file:
            try:
                py_compile.compile(code_file)
                result = True
            except SyntaxError as e:
                result = False
        return (int(result), "Compilation " + ["Failed", "Succeeded"][result])

if __name__ == "__main__":
    groups = utils.load_json("groups.json")
    submissions = utils.load_json("students.json")
    submissions = utils.convert_submission_dict_to_classes(submissions)
    groups = utils.generate_group_submissions(submissions, groups)
    grader = GroupSubmissionGrader()
    grader.check_groups(groups)
