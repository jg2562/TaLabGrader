from gradeHandler import GradeHandler
from report import Report
from submission import Submission
from os.path import exists

class Lab:
    def __init__(self, name, submissions=[], comment=""):
        self._report = None
        self._code = None

        self._student_name = name.strip()
        self._misc_files = []
        self._comment = comment
        self._partners = []
        nameS = name.strip().lower().split(" ")
        self._lab_name = "".join(nameS[1:]) + nameS[0]
        self.add_submission(submissions)


    def _set_file(self, submission):
        submission_type = submission.get_type()
        if submission_type in ["pdf", "docx"]:
            self._report = Report(submission.get_file())
        elif submission_type == "py":
            self._code = submission

    def add_partner_lab(self, lab):
        self._partners.append(lab)

    def add_submission(self, submissions):
        for submission in submissions:
            self._set_file(Submission(submission))
        self._misc_files += submissions

    def get_student_name(self):
        return self._student_name

    def get_lab_name(self):
        return self._lab_name

    def get_lab_report(self):
        return self._report


class LabHandler:
    def __init__(self):
        self._labs = {}

    def add_lab(self, lab):
        self._labs[lab.get_lab_name()] = lab

    def pair_all_labs(self):
        for student in self._labs:
            self.get_lab_pairings(self._labs[student])

    def get_lab_pairings(self, lab):
        for other_lab in self._labs.values():
            if self.is_partner(lab, other_lab):
                lab.add_partner_lab(other_lab)

    def is_partner(self, lab, other_lab):
        return lab.get_lab_report().contains_string(other_lab.get_student_name())


if __name__ == "__main__":
    gh = GradeHandler()
    lh = LabHandler()
    for student in gh.get_all_students():
        lab = Lab(student)
        file_combs = [("code", "py"), ("report", "pdf"), ("report", "docx")]
        submissions = [submission for submission in ["./" + file_part[0] + "/" + lab.get_lab_name() + "_0." + file_part[1] for file_part in file_combs] if exists(submission)]
        lab.add_submission(submissions)
        if submissions:
            lh.add_lab(lab)

    lh.pair_all_labs()
    print("Done")