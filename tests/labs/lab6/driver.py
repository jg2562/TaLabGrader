import os
import sys
import importlib.util
from io import StringIO
from contextlib import redirect_stdout

def import_file(filename):
    filename = os.path.abspath(filename)
    mname = os.path.splitext(os.path.basename(filename))[0]
    spec = importlib.util.spec_from_file_location(mname, filename)
    modulename = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulename)
    return modulename

def run_tests(testmodule, studentcode):
    score = 0
    for test in get_test_functions(testmodule):
        try:
            results = test[0](studentcode)
            if not results[0]:
                return (score, results[1])
            score += test[1]
        except Exception as e:
            return (score, "Exception thrown in test: {}".format(test[2]))
    return (score, "")

def get_test_functions(testmodule):
    tests = testmodule.get_test_functions()
    return tests

if __name__ == "__main__":
    out = StringIO()
    with redirect_stdout(out):
        testmodule = import_file(sys.argv[1])
        studentcode = import_file(sys.argv[2])
        results = run_tests(testmodule, studentcode)
    print(results[0])
    print(results[1])
