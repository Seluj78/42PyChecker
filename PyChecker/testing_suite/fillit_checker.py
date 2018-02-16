"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import subprocess
from PyChecker.utils import git

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
    result = subprocess.run(['bash', root_path + '/scripts/clean_logfiles.sh', root_path + '/.myfillitchecker'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8')
    with open(root_path + '/.myfillitchecker', 'r') as file:
        print(file.read())
        for line in file:
            if "NOTE" in line:
                return line
