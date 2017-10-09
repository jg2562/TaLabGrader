import openpyxl
import grader.utils as utils

class GradeSheet():
    def __init__(self, workbook_name=""):
        self.workbook_name = workbook_name
        self._active_sheet = None
        try:
            self.wb = openpyxl.load_workbook(workbook_name)
        except FileNotFoundError:
            self.wb = openpyxl.Workbook()

    def create_grade_sheet(self, groups, lab_config, group_grades):
        lab_config = lab_config["assignment"]
        lab_name = lab_config["lab name"]
        lab_sheet = self._get_lab_sheet(lab_name)
        self._section_ranges = self._get_section_ranges(lab_config["sections"])
        self._active_sheet = lab_sheet
        self._setup_header(lab_config)
        self._create_group_rows(lab_config, groups, group_grades)
        self.wb.save(self.workbook_name)

    def _get_lab_sheet(self, lab_name):
        if lab_name not in self.wb.sheetnames:
            return self.wb.create_sheet(title=lab_name)
        else:
            return self.wb.get_sheet_by_name(lab_name)

    def _get_section_ranges(self, sections):
        # skip lab name, total col
        column = 3
        ranges = {}
        for section in sections:
            start = column
            end = len(section["criteria"]) + start - 1
            ranges[section["name"]] = (start, end)
            column = end + 2
        return ranges

    def _setup_header(self, lab_config):
        self._active_sheet.cell(column=1,row=1).value = lab_config["lab name"]
        self._active_sheet.cell(column=2,row=1).value = "Total"

        sections_config = lab_config["sections"]
        for section in lab_config["sections"]:
            section_range = self._section_ranges[section["name"]]
            self._setup_section_header(section["criteria"], section_range)

    def _setup_section_header(self, section_config, section_range):
        for column, criteria in enumerate(section_config):
            cell = self._active_sheet.cell(column=column + section_range[0], row=1)
            cell.value = criteria["name"]
            cell.comment = openpyxl.comments.Comment("{}:{}".format(criteria["worth"], criteria["description"]), "Auto-Generator")

    def _create_group_rows(self, lab_config, groups, group_grades):
        for group_num in groups:
            self._create_group_row(lab_config, int(group_num) + 2, groups[int(group_num)], group_grades[group_num])

    def _create_group_row(self, lab_config, row_num, group, group_grade):
        self._active_sheet.cell(column=1, row=row_num).value = "Group {}".format(group.get_group_number())
        sum_val = self._build_sum_formula(lab_config["sections"], row_num)
        self._active_sheet.cell(column=2, row=row_num).value = sum_val

        self._add_auto_grades(lab_config["sections"], row_num, group_grade)

    def _build_sum_formula(self, sections, row_num):
        sums = []
        col_letter = openpyxl.utils.get_column_letter
        for section in sections:
            if section["include"]:
                start = col_letter(self._section_ranges[section["name"]][0])
                end = col_letter(self._section_ranges[section["name"]][1])

                sums.append("SUM({}{}:{}{})".format(start, row_num,
                                                   end, row_num))
        return "=" + " + ".join(sums)


    def _add_auto_grades(self, sections, row_num, group_grade):
        for section in sections:
            for i, criteria in enumerate(section["criteria"]):
                if "test" in criteria and criteria["test"] in group_grade:
                    test_name = criteria["test"]
                    column = self._section_ranges[section["name"]][0] + i
                    cell = self._active_sheet.cell(column=column, row=row_num)
                    grade = group_grade[test_name]
                    cell.value = grade[0] * criteria["possible"]
                    cell.comment = openpyxl.comments.Comment(str(grade[1]), "Auto-Grader")
