
class GroupSubmission():

    def __init__(self, group_number, groups, submissions):
        self.number = group_number
        self.members = groups[group_number]
        member_submission = submissions[self.members[0]]
        self.code = member_submission.get_code()
        self.report = member_submission.get_report()

    def get_code(self):
        return self.code

    def get_report(self):
        return self.code

    def get_members(self):
        return self.members

    def get_group_number(self):
        return self.number
