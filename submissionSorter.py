import utils
import os.path as path
import os
import shutil


class SubmissionSorter:
    def __init__(self, submissions, groups):
        self.submissions = submissions
        self.groups = groups

    def create_group_submissions(self, groups_dir):

        for group_number in self.groups:
            group = self.groups[group_number]
            student = self.submissions[group[0]]
            group_dir_name = "group_" + str(group_number)
            group_dir = path.join(groups_dir, group_dir_name)
            os.makedirs(group_dir, exist_ok=True)
            if student.get_code():
                shutil.copy(student.get_code(),
                            path.join(group_dir, "code.py"))
            if student.get_report():
                shutil.copy(student.get_report(),
                            path.join(group_dir, "report.pdf"))


if __name__ == "__main__":
    groups = utils.load_json("groups.json")
    submissions = utils.load_json("students.json")
    submissions = utils.convert_submission_dict_to_classes(submissions)
    sorter = SubmissionSorter(submissions, groups)
    sorter.create_group_submissions("./groups/")
