import subprocess
import os
from os import path

class TestSuite():
    def __init__(self, lab_config):
        raw_tests = lab_config['testing']
        self._tests = []

        for test_group in raw_tests:
            if not path.exists(test_group["driver"]):
                raise FileNotFoundError("Driver file not found: {}".format(test_group["driver"]))
            for test in test_group["tests"]:
                self._tests.append(TestRunner(test, test_group))

    def run_tests(self, code_file):
        results = {}
        for test in self._tests:
            result = test.run_test(code_file)
            results[test.get_test_name()] = result
        return results

class TestRunner():
    def __init__(self, test_config, test_group_config):
        self._driver_file = path.abspath(test_group_config["driver"])
        self._test_file = path.abspath(path.join(test_group_config["testing dir"], test_config["file"]))
        self._test_name = test_config["name"]
        if not path.exists(self._test_file):
            raise FileNotFoundError("Test file not found: {}".format(config["name"]))

    def get_test_name(self):
        return self._test_name

    def run_test(self, code_file):
        if not path.exists(path.abspath(code_file)):
            raise FileNotFoundError("Code file not found: {}".format(code_file))
        args = ["python3", self._driver_file, self._test_file, path.abspath(code_file)]
        cprocess = subprocess.Popen(args, stdout=subprocess.PIPE)
        return self._get_test_result(cprocess)

    def _get_test_result(self, cprocess):
        lines = [ bytestr.decode() for bytestr in cprocess.stdout.readlines()]
        score = int(lines[0])
        return (score, ("".join(lines[1:]).strip()))
