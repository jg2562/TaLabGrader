import re
import openpyxl

class CommentGenerator():

    def add_comments_to_sheet(self, submissions, lab, wb):
        comment_map = {username: self._generate_student_comment(submissions[username], submissions) for username in submissions}
        self._comment_map_to_sheet(wb, lab, comment_map)

    comment_regex = re.compile("[0-2]")
    def _generate_student_comment(self, submission, sub_map):
        partners = submission.get_partners()
        comments = [sub_map[partner].get_comment().strip() for partner in partners if partner in sub_map and sub_map[partner].get_comment()]
        value = "-"
        if len(comments) == 1:
            matches = self.comment_regex.findall(comments[0])
            if len(matches) == 1:
                value = matches[0]
        return (value, "\n---\n".join(comments))

    def _comment_map_to_sheet(self, workbook_name, lab, comment_map):
        wb = openpyxl.load_workbook(workbook_name)
        sheet = wb["Comments"]
        username_col = [cell for cell in sheet["C"][1:] if cell.value]
        lab_col_num = [cell.value for cell in sheet[1]].index("Lab " + str(lab))
        for username_cell in username_col:
            cell = sheet.cell(column=lab_col_num, row=username_cell.row)
            try:
                com = comment_map[username_cell.value]
                cell.value = com[0]
                if com[1]:
                    cell.comment = openpyxl.comments.Comment(com[1], "Auto-Grader")
            except KeyError:
                cell.value = "-"
        wb.save(workbook_name)
