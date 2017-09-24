import os
import os.path
import zipfile

class SubmissionGenerator:
    def __init__(self, config):
        self._config = config

    def generate_submissions(self):
        self._generate_submission_files()
        return self._generate_info_file()


    def _generate_submission_files(self):
        zip_filename = self._config['zip file']
        sub_root_dir = self._config["submissions dir"]
        if not zipfile.is_zipfile(zip_filename):
            raise ValueError("Bad submissions zip file: {}".format(zip_filename))

        with zipfile.ZipFile(zip_filename) as subzip:
           for submission_file in subzip.infolist():
               sub_parts = submission_file.filename.split("_")
               sub_username = sub_parts[1]
               sub_user_dir = os.path.join(sub_root_dir, sub_username)
               os.makedirs(sub_user_dir, exist_ok=True)
               subzip.extract(submission_file, path=sub_user_dir)

    def _generate_info_file(self):
        submissions = {}
        for root, paths, files in os.walk(self._config["submissions dir"]):
            for filename in files:
                sub_parts = filename.split("_")
                extension = sub_parts[-1].split(".")[1]
                if len(sub_parts) == 4 and extension == "txt":
                    info_filename = os.path.join(root, filename)
                    submission = self._get_submission_info(info_filename)
                    submission['dir'] = root
                    submissions[submission['username']] = submission
                    os.remove(info_filename)
        return submissions


    def _get_submission_info(self, info_filename):
        submission = {}
        with open(info_filename, 'r') as fh:
            file_lines = fh.readlines()
        file_lines = [line.encode('ascii', errors='ignore').decode().strip() for line in file_lines]
        name_parts = file_lines[0].split(':')[1].split(" ")
        submission['name'] = " ".join(name_parts[:-1]).strip()
        submission['username'] = name_parts[-1].strip()[1:-1]
        submission['date'] = ":".join(file_lines[2].split(":")[1:]).strip()

        comment = file_lines[file_lines.index("Comments:") + 1]
        if comment == "There are no student comments for this assignment.":
            comment = ""
        submission['comment'] = comment
        return submission
