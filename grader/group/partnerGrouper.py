import json
import filecmp
from grader.submission.submission import Submission

class PartnerGrouper():
    def __init__(self, submissions):
        self.submissions = submissions

    def generate_group_submissions(self, generate_groups):
        groups = generate_groups()
        # TODO: Finish this, so it return group classes

    def generate_groups(self):
        groups = []
        ungrouped_students = {student for student in self.submissions}
        while ungrouped_students:
            student = ""
            for student_e in ungrouped_students:
                if student_e > student:
                    student = student_e
            group = self.generate_group_from_student(student)
            groups.append(list(group))
            ungrouped_students -= group

        indexed_groups = {}
        for index, group in enumerate(groups):
            indexed_groups[index] = group

        return indexed_groups

    def generate_group_from_student(self, student):
        group = set()
        group.add(student)
        student_submission = self.submissions[student]
        for partner in student_submission.get_partners():
            if partner in self.submissions:
                partner_sub = self.submissions[partner]
                if student_submission.is_partner(partner_sub):
                    group.add(partner)
        return group
