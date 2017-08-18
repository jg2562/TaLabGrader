from submission import Submission

class PartnerGrouper():
    def __init__(self, submissions):
        self.submissions = {}
        for student in submissions:
            self.submissions = Submission(submissions[student])

    def generate_groups(self):
        groups = []
        ungrouped_students = {student for student in submissions}
        while ungrouped_students:
            student = ungrouped_students.pop()
            group = generate_group_from_student(student)
            groups.append(list(group))
            ungrouped_students -= group
        return groups

    def generate_group_from_student(self, student):
        group = set()
        group.add(student)
        student_submission = self.submissions[student]
        for partner in student_submission.get_partners():
            partner_sub = submissions[partner]
            if student_submission.is_partner(partner_sub):
                group.add(partner)
        return group
