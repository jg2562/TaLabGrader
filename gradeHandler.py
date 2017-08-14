import openpyxl


class GradeHandler:
    def __init__(self):
        wb_name = 'Grading.xlsx'
        self._grades = {}

        sheet = self._get_work_sheet(wb_name)
        self._load_grades(sheet)

    def _get_work_sheet(self, workbook_name):
        wb = openpyxl.load_workbook(workbook_name, data_only=True)
        sheet = wb.get_sheet_by_name("Sheet1")
        return sheet

    def _load_grades(self, sheet):

        # lab = input("What lab is this: ").strip().capitalize()
        row = 2
        name = sheet.cell(row=row, column=1).value
        while name:
            name = name.split(",")
            name = name[1].strip() + " " + name[0].strip()
            self._grades[name] = {}
            self._grades[name]["Grade"] = str(sheet.cell(row=row, column=4).value)
            com = sheet.cell(row=row, column=4).comment
            if com is not None:
                self._grades[name]["Note"] = str(com.text)
            elif self._grades[name]["Grade"] == "-":
                self._grades[name]["Note"] = ""
            else:
                raise ValueError("No note found on {}".format(name))
            row += 1
            name = sheet.cell(row=row, column=1).value

    def get_grade(self, name):
        return self._grades[name]["Grade"]

    def get_note(self, name):
        return self._grades[name]["Note"]

    def get_all_students(self):
        return self._grades.keys()

