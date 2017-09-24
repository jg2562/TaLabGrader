import re
import filecmp

class Submission():
    def __init__(self, submission_dict):
        self.username = submission_dict["username"]
        self.student_name = submission_dict["name"]
        self.attachments = submission_dict["attachments"]
        self.comment = submission_dict["comment"]
        self.report = None
        self.code = None

        for attachment in self.attachments:
            extension = attachment.split(".")[-1]
            if extension == "pdf":
                self.report = attachment
            elif extension == "py":
                self.code = attachment

        self.partners = self._generate_partner_usernames()

    username_regex = re.compile("[a-zA-Z]{2,4}[0-9]{1,6}")
    def _generate_partner_usernames(self):
        if not self.code:
            return []
        code_fh = open(self.code, "r")
        code = "\n".join(code_fh.readlines())
        matches = [match.lower() for match in re.findall(self.username_regex, code)]
        bad_matches = ["cs126", self.username]
        matches = [match for match in matches if match not in bad_matches]
        return matches

    def get_name(self):
        return self.student_name

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
        return self.is_bidirectional_partnership(partner) and self.has_same_attachments(partner)

    def is_bidirectional_partnership(self, partner):
        return self.get_username() in partner.get_partners()

    def has_same_attachments(self, partner):
        # TODO: Figure out same report idea
        return self.has_same_code(partner) # and self.has_same_report(partner)

    def has_same_code(self, partner):
        return self.is_same_file(self.get_code(), partner.get_code())

    def has_same_report(self, partner):
        return self.is_same_file(self.get_report(), partner.get_report())

    def is_same_file(self, file1, file2):
        if file1 and file2:
            return filecmp.cmp(file1, file2)
        return False
