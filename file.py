class Submission():
    def __init__(self, submission):
        self._submission = submission

    def get_submission_type(self):
        return self._report.split(".")[1]

    
