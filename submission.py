from os.path import abspath

class Submission():
    def __init__(self, submission):
        self._submission = abspath(submission)

    def get_type(self):
        return self._submission.split(".")[1]

    def get_file(self):
        return self._submission

