import py_compile
import sys
from pycodestyle import StyleGuide

def check_pep8(code_file):
    style_guide = StyleGuide(quiet=True)
    result = (0, [])
    if code_file:
        pep8_report = style_guide.check_files([code_file])
        result = (int(pep8_report.get_file_results()), pep8_report.get_statistics())
    return (result[0] > 5, "\n".join(result[1]))

def get_test_functions():
    return [(check_pep8, 1, "Not pep8 compliant")]
