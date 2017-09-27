import subprocess
from os import path

class CheatDetector():
    def __init__(self, config):
        pass

    def _runMoss(self, groups, basefile):
        groups_code = list(map(lambda x: groups[x].get_code(), groups))
        moss_file = path.join(path.dirname(__file__), "moss.pl")
        args = ["perl", moss_file] + groups_code
        print(args)
        cprocess = subprocess.Popen(args, stdout=subprocess.PIPE)
        stdout = cprocess.communicate()[0].decode("utf-8")
        moss_url = stdout.split("\n")[-2]
        print("Moss url: {}".format(moss_url))

    def checkGroups(self):
        pass
