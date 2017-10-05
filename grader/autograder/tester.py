import subprocess
import os
from os import path

class TestSuite():
    def __init__(self, config):
        self._test_dir = config['test dir']
        self._tests = []
        for root, folders, files in os.walk(self._test_dir):
            for test_name in files:
                abs_test_name = path.abspath(path.join(root, filename))
                self._tests.append(TestRunner(config, abs_test_name))

    def run_tests(self, code_file):
        results = {}
        for test in self._tests:
            result = test.run_test(code_file)
            results[test.get_test_name] = result
        return results

class TestRunner():
    def __init__(self, config, test_file):
        self._config = config
        self._test_file = test_file
        self._test_name = os.path.splitext(os.path.basename(test_file))[0]

    def get_test_name(self):
        return self._test_name

    def run_test(self, code_file):
        args = ["python", path.abspath(self._test_file), path.abspath(code_file)]
        cprocess = subprocess.Popen(args, stdout=subprocess.PIPE)
        return self._get_test_result(cprocess)

    def _get_test_result(self, cprocess):
        result = int(cprocess.stdout)
        return result
