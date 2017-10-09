import openpyxl
import json

if __name__ == "__main__":
    row = 8
    wb = openpyxl.load_workbook("./data/rubric.xlsx")
    sheet = wb.active
    cats = []
    for col in sheet[row][1:]:
        if col.value:
            cat = {"name" : "", "description": col.comment.text, "worth": int(col.value), "possible": int(col.value), "test": ""}
            cats.append(cat)
    print(json.dumps(cats, indent=4, separators=(',', ': ')))
