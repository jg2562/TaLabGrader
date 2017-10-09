import os
import sys
import importlib.util

def import_file(filename):
    filename = os.path.abspath(filename)
    mname = os.path.splitext(os.path.basename(filename))[0]
    spec = importlib.util.spec_from_file_location(mname, filename)
    modulename = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulename)
    return modulename

def run_tests(testmodule, studentcode):
    for test in get_test_functions(testmodule):
        try:
            results = test[0](studentcode)
            if results[0]:
                return (1, "Pep8 errors")
        except Exception as e:
            return (score, "Exception thrown in test: {}".format(test[2]))

    return (0, "")

def get_test_functions(testmodule):
    tests = testmodule.get_test_functions()
    return tests

if __name__ == "__main__":
    testmodule = import_file(sys.argv[1])
    studentcode = sys.argv[2]
    results = run_tests(testmodule, studentcode)
    print(results[0])
    print(results[1])
