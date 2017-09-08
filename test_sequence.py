import utils
from partnerGrouper import PartnerGrouper
from submissionSorter import SubmissionSorter
from gradeSheet import GradeSheet

def students_to_sheet(submissions):
    lab_sheet_name = "grading-sheet.xlsx"
    rubric_name = "rubric.xlsx"
    lab_number = 10
    groups = PartnerGrouper(submissions).generate_groups()
    submissions = utils.convert_submission_dict_to_classes(submissions)
    SubmissionSorter(submissions, groups).create_group_submissions("./groups/")
    groups = utils.generate_group_submissions(submissions, groups)
    GradeSheet(lab_sheet_name).create_grade_sheet(groups, rubric_name, lab_number)


if __name__ == "__main__":
    submissions = utils.load_json("students.json")
    students_to_sheet(submissions)

# Check if they even have a code file
