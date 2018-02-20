"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import os
import subprocess
from PyChecker.utils import git
import logging


def replace_my_config(root_path: str, project_path: str):
    logging.info("LIBFTEST: Replacing config file with correct parameters")
    logging.debug("LIBFTEST: Opening file {}.".format(root_path + "/testing_suites/libftest/my_config.sh"))
    with open(root_path + "/testing_suites/libftest/my_config.sh", 'w+') as file:
        file.write('# !/bin/bash' + '\n')
        file.write('PATH_LIBFT=' + project_path + '\n')
        file.write('PATH_DEEPTHOUGHT=' + root_path + '\n')
        file.write('COLOR_OK="${GREEN}"' + '\n')
        file.write('COLOR_FAIL="${RED}"' + '\n')
        file.write('COLOR_WARNING="${YELLOW}"' + '\n')
        file.write('COLOR_TITLE="${BOLD}${BLUE}"' + '\n')
        file.write('COLOR_FUNC="${CYAN}"' + '\n')
        file.write('COLOR_PART="${UNDERLINE}${PURPLE}"' + '\n')
        file.write('COLOR_TOTAL="${BOLD}${YELLOW}"' + '\n')
        file.write('COLOR_DEEPTHOUGHT_PATH="${BOLD}${PURPLE}"' + '\n')


def run(project_path: str, root_path: str):
    """
    This function runs the libftest to the given project.

    :param project_path: The path of the project you want to test.
    """

    logging.info("Starting libftest testing suite checks.")
    if "fatal: Not a git repository" in git.status(root_path + '/testing_suites/libftest'):
        git.clone("https://github.com/jtoty/libftest.git", root_path + '/testing_suites/libftest')
    else:
        git.reset(root_path + '/testing_suites/libftest')

    print("*---------------------------------------------------------------*")
    print("*----------------------------Libftest---------------------------*")
    print("*---------------------------------------------------------------*")

    replace_my_config(root_path, project_path)
    logging.debug("LIBFTEST: Running `bash {} -l -s -f -n -u`".format(root_path + "/testing_suites/libftest/grademe.sh"))
    result = subprocess.run(['bash', root_path + "/testing_suites/libftest/grademe.sh",
                             "-l -s -f -n -u"], stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).stdout.decode('utf-8')
    logging.debug("LIBFTEST: Renaming deepthought file")
    os.rename(root_path + "/deepthought", root_path + "/.mylibftest-deepthought")
    print("Deepthought file too big. Not printed. See `.mylibftest-deepthought'.")

    logging.debug("LIBFTEST: Opening file {}.".format(root_path + "/.mylibftest"))
    with open(root_path + "/.mylibftest", 'w+') as file:
        file.write("*------------------------------------------------------*\n")
        file.write("LIBFTEST\n")
        file.write("Warning: This file contains escape sequences. Please use "
                   "`cat' to view it properly.\n")
        file.write("*------------------------------------------------------*\n")
        file.write(result)

    print(result)
    logging.debug("LIBFTEST: Opening file {}.".format(root_path + "/.mylibftest"))
    with open(root_path + "/.mylibftest", 'r') as file:
        res = ""
        for line in file:
            if "Total : " in line:
                res += line
    totals = res.split('\n')
    logging.info("Finished libftest testing suite checks.")
    return totals
