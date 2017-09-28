import subprocess
from os import path
import requests
import bs4
import re

class CheatDetector():
    def __init__(self, config):
        self._config = config

    def get_cheat_mapping(self, groups, basefile, lower_cutoff, upper_cutoff):
        moss_url = self._run_moss(groups, basefile)
        rating_mapping = self._get_cheat_map_from_url(moss_url, cutoff)
        return rating_mapping

    def _get_cheat_map_from_url(self, moss_url, lower_cutoff, upper_cutoff):
        soup = self._soupify_moss(moss_url)
        group_data = self._parse_soup(soup)
        culled_data = self._cull_groups_data(group_data, lower_cutoff, upper_cutoff)
        rating_mapping = self._create_ratings_mapping(culled_data)
        return rating_mapping

    def _run_moss(self, groups, basefile):
        groups_code = list(map(lambda x: groups[x].get_code(), groups))
        moss_file = path.join(path.dirname(__file__), "moss.pl")
        args = ["perl", moss_file, "-l", "python", "-d", path.join(self._config["groups dir"], "*/code.py")]
        if basefile:
            args += [" ".join("-b", basefile)]
        cprocess = subprocess.Popen(" ".join(args), shell=True, stdout=subprocess.PIPE)
        stdout = cprocess.communicate()[0].decode("utf-8")
        moss_url = stdout.split("\n")[-2]
        return moss_url

    def _soupify_moss(self, moss_url):
        r = requests.get(moss_url)
        soup = bs4.BeautifulSoup(r.content.decode('utf-8'), 'lxml')
        return soup

    def _parse_soup(self, soup):
        table = soup.find("table")
        pattern = re.compile("\.\/data\/group\/group_([0-9]+)\/ \(([0-9]+)\%\)")
        groups_data = list(filter(lambda x: x,map(lambda x: self._get_group_rating(x.find_all("a"), pattern), table.find_all("tr"))))
        return groups_data

    def _get_group_rating(self, links, pattern):
        if links:
            matches = map(lambda x: pattern.match(x.string), links)
            total_data = list(map(lambda x: (int(x.group(1)), int(x.group(2))), matches))
            group_data = (total_data[0][0], total_data[1][0], max(total_data[0][1], total_data[1][1]))
            return group_data

    def _cull_groups_data(self, groups_data, lower_cutoff, upper_cutoff):
        return list(filter(lambda x: lower_cutoff < x[2] < upper_cutoff, groups_data))

    def _create_ratings_mapping(self, groups_data):
        ratings = {}
        for group in groups_data:
            if group[0] not in ratings:
                ratings[group[0]] = {}
            if group[1] not in ratings:
                ratings[group[1]] = {}
            ratings[group[0]][group[1]] = group[2]
            ratings[group[1]][group[0]] = group[2]
        return ratings

