import openpyxl
import grader.utils as utils
from grader.submission.submissionChecks import GroupSubmissionGrader

class GradeSheet():
    def __init__(self, workbook_name=""):
        self.workbook_name = workbook_name
        try:
            self.wb = openpyxl.load_workbook(workbook_name)
        except FileNotFoundError:
            self.wb = openpyxl.Workbook()

    def create_grade_sheet(self, groups, lab_config):
        lab_name = lab_config["assignment"]["lab name"]

        lab_sheet = None
        if lab_name not in self.wb.sheetnames:
            lab_sheet = self.wb.create_sheet(title=lab_name)
        else:
            lab_sheet = self.wb.get_sheet_by_name(lab_name)
        self._sections = lab_config["assignment"]["section order"]
        self._setup_header(lab_sheet, lab_config["assignment"])
        self._create_group_rows(lab_sheet, lab_config, groups)
        self.wb.save(self.workbook_name)

    def _setup_header(self, lab_sheet, lab_config):
        lab_sheet.cell(column=1,row=1).value = lab_config["lab name"]
        lab_sheet.cell(column=2,row=1).value = "Total"
        self._section_ranges = {}
        column = 3
        sections_config = lab_config["sections"]
        for sub_header in self._sections:
            header_range = self._setup_sub_header(lab_sheet, sections_config[sub_header], column)
            self._section_ranges[sub_header] = header_range
            column = header_range[1] + 2

    def _setup_sub_header(self, lab_sheet, section_config, column):
        start = column
        for section in section_config:
            cell = lab_sheet.cell(column=column, row=1)
            cell.value = section["name"]
            cell.comment = openpyxl.comments.Comment("{}:{}".format(section["points"], section["description"]), "Auto-Generator")
            column += 1
        return (start, column - 1)

    def _create_group_rows(self, lab_sheet, lab_config, groups):
        group_grades = GroupSubmissionGrader().check_groups(groups)
        for group_num in groups:
            self._create_group_row(lab_sheet, lab_config["assignment"], int(group_num) + 2, groups[int(group_num)], group_grades[group_num])

    def _create_group_row(self, lab_sheet, lab_config, row_num, group, group_grade):
        lab_sheet.cell(column=1, row=row_num).value = "Group {}".format(group.get_group_number())
        col_letter = openpyxl.utils.get_column_letter
        sum_val = "=SUM({}{}:{}{})".format(col_letter(self._section_ranges["report"][0]), row_num,
                                           col_letter(self._section_ranges["other"][1]), row_num)
        lab_sheet.cell(column=2, row=row_num).value = sum_val

        for column in range(self._section_ranges["penalities"][0], self._section_ranges["penalities"][1] + 1):
            cell = lab_sheet.cell(column=column, row=row_num)
            cell.value = 0

        sections = lab_config["sections"]
        for section in self._sections:
            for i, criteria in enumerate(sections[section]):
                criteria_name = criteria["name"]
                if criteria_name in group_grade:
                    column = self._section_ranges[section][0] + i
                    cell = lab_sheet.cell(column=column, row=row_num)
                    grade = group_grade[criteria_name]
                    cell.value = grade[0]
                    cell.comment = openpyxl.comments.Comment(str(grade[1]), "Auto-Grader")

    def _extract_pep8(self, group_grades):
        errors = group_grades["Pep8"]
        return (errors[0], "\n".join(errors[1]))

    def _extract_partner_grade(self, group_grades):
        # Needs to be per-student basis
        return ("-", None)

    def _extract_syntax(self, group_grades):
        compiles = group_grades["Syntax"]
        return (int(compiles), "Compilation " + ["Failed", "Completed"][compiles])

if __name__ == "__main__":
    submissions = utils.load_json("students.json")
    submissions = utils.convert_submission_dict_to_classes(submissions)
    groups = utils.load_json("groups.json")
    groups = utils.generate_group_submissions(submissions, groups)
    lab_number = 10
    rubric_name = "rubric.xlsx"
    lab_sheet_name = "grading-sheet.xlsx"
    GradeSheet(lab_sheet_name).create_grade_sheet( groups, rubric_name, lab_number)
