import re
import filecmp

class Submission():
    def __init__(self, submission_dict):
        self.username = ""
        self.student_name = submission_dict["name"]
        self.attachments = submission_dict["attachments"]
        self.comment = submission_dict["comment"]
        self.report = None

        for attachment in self.attachments:
            extension = attachment.split(".")[-1]
            if extension == "pdf":
                self.report = attachment
            elif extension == "py":
                self.code = attachment

        self.partners = self._generate_partners()

    username_regex = re.compile("[a-zA-Z]{2,3}[0-9]{2,4}")
    def _generate_partner_usernames(self):
        code_fh = open(self.code, "r")
        code = code_fh.readlines().join("\n")
        matches = re.findall(username_regex, code)

        return [match.group(0) for match in matches]

    def get_name(self):
        return self.name

    def get_username(self):
        return self.username

    def get_comment(self):
        return self.comment

    def get_report(self):
        return self.report

    def get_code(self):
        return self.code

    def get_partners(self):
        return self.partners

    def is_partner(self, partner):
        return is_bidirectional_partnership(student, partner) and has_same_attachments(partner)

    def is_bidirectional_partnership(self, partner):
        return self.get_username() in partner.get_partners()

    def has_same_attachments(self, partner):
        return has_same_code() and has_same_report()

    def has_same_code(self, partner):
        return is_same_file(self.get_code(), partner.get_code())

    def has_same_report(self, partner):
        return is_same_file(self.get_report(), partner.get_report())

    def is_same_file(file1, file2):
        return filecmp.cmp(file1, file2)
