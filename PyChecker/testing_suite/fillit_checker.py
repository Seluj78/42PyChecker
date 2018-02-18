"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import subprocess
from PyChecker.utils import git
import re
import os


def clean_log(root_path: str):
    with open(root_path + '/.myfillitchecker-clean', 'w+') as file2:
        with open(root_path + '/.myfillitchecker', 'r') as file:
            for line in file:
                line = re.sub(r"\033\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]/", "", line)
                file2.write(line)
                print(line)
    #os.rename(root_path + '/.myfillitchecker-clean', root_path + '/.myfillitchecker')
    #return


def run(root_path: str, project_path: str):
    """
    This function runs the fillit_checker to the given project.

    :param project_path: The path of the project you want to test.
    """
    print("*---------------------------------------------------------------*")
    print("*-------------------------fillit_checker------------------------*")
    print("*---------------------------------------------------------------*")

    if "fatal: Not a git repository" in git.status(root_path + '/testing_suites/fillit_checker'):
        git.clone("https://github.com/anisg/fillit_checker", root_path + '/testing_suites/fillit_checker')
    else:
        git.reset(root_path + '/testing_suites/fillit_checker')

    # @todo: Find a way to supress colors from output
    result = subprocess.run(['bash', root_path + "/testing_suites/fillit_checker/test.sh", project_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8')
    with open(root_path + '/.myfillitchecker', 'w+') as file:
        file.write(result)
    clean_log(root_path)
    #with open(root_path + '/.myfillitchecker', 'r') as file:
    #    print(file.read())
    #    for line in file:
    #        if "NOTE" in line:
    #            return line
