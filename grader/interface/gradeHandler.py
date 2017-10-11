import openpyxl
import grader.utils as utils

class GradeHandler:
    def __init__(self, config, groups, students, lab_number, sheet_grades):
        self._config = config
        self._group_grades = {}
        self._grades = {}

        self._load_student_grades(groups, students, sheet_grades)

    def _load_student_grades(self, groups, students, group_grades):
        for group in group_grades:
            for student in groups[str(group)]:
                student_grade = {}
                group_grade = self._get_group_grade(group, group_grades)
                student_penalties = self._get_student_penalties(students[student])

                for category in group_grades[group]:
                    student_grade[category] = group_grade[category] + student_penalties[category]

                pleasantries = self._get_pleasantries(student_grade["Grade"])
                for category in group_grades[group]:
                    student_grade[category] += pleasantries[category]

                student_grade["Grade"] = max(0, student_grade["Grade"])
                student_grade["Note"] = ("\n".join(filter(lambda x: x, student_grade["Note"]))).strip()
                self._grades[student] = student_grade

    def _get_group_grade(self, group, group_grades):
        grade = group_grades[group]
        new_grade = {}
        new_grade["Grade"] = grade["Grade"]
        new_grade["Note"] = [grade["Note"]]
        return new_grade

    def _get_student_penalties(self, student):
        penalties = {}
        prelab = self._get_prelab_penalties(student)
        ratings = self._get_partner_rating_penalties(student)
        penalties["Grade"] = prelab[0] + ratings[0]
        penalties["Note"] = [prelab[1], ratings[1]]
        return penalties

    def _get_prelab_penalties(self, student):
        if True:
            return (0, "")
        else:
            return (-3, "-3: No Prelab")

    def _get_partner_rating_penalties(self, student):
        if student["comment"].strip():
            return (0, "")
        else:
            return (-2, "-2: No partner rating")

    def _get_pleasantries(self, group_grade):
        pleasant = {}
        comments = []
        grade = group_grade
        if grade >= 36:
            comments += [self._config["grader A compliment"]]
        elif grade >= 32:
            comments += [self._config["grader B compliment"]]
        comments += ["-" + self._config["grader name"]]
        pleasant["Grade"] = 0
        pleasant["Note"] = comments
        return pleasant

    def contains_student(self, name):
        return name in self._grades

    def get_grade(self, name):
        try:
            return str(self._grades[name]["Grade"])
        except KeyError:
            return None

    def get_comment(self, name):
        try:
            return self._grades[name]["Note"]
        except KeyError:
            return None

    def get_all_students(self):
        return self._grades.keys()
