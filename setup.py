from setuptools import setup

setup(name='Grader',
      version='1.0',
      description='Simplifies grading in BBlearn',
      author='Jack Garrard',
      author_email='jg2562@nau.edu',
      url='https://github.com/jg2562/TaLabGrader',
      packages=['grader', 'grader.autograder', 'grader.browser',
                'grader.group', 'grader.interface', 'grader.load', 'grader.submission'],
      package_data={'grader.autograder':['moss.pl']},
      requires=['openpyxl','splinter','request','pycodestyle'])
