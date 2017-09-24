import code
import grader.utils as utils
from grader.browser.gradeBrowser import GradeBrowser

if __name__ == "__main__":
    config = utils.load_json("config/general.json")
    browser = GradeBrowser(config)
    code.interact(local=locals())
