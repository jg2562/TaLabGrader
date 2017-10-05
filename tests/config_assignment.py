import openpyxl
import json

if __name__ == "__main__":
    row = 5
    wb = openpyxl.load_workbook("./data/grade-sheet.xlsx")
    sheet = wb.get_sheet_by_name("Rubric")
    cats = []
    for col in sheet[row][1:]:
        if col.value:
            cat = {"name" : "", "description": col.comment.text, "points": col.value, "test": ""}
            cats.append(cat)
    print(json.dumps(cats, indent=4, separators=(',', ': ')))
