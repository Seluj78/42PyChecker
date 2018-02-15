"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import os
import subprocess

from tempfile import mkstemp
from shutil import move
from os import fdopen, remove


def replace_my_config(root_path: str, project_path: str):
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
    print("*---------------------------------------------------------------*")
    print("*----------------------------Libftest---------------------------*")
    print("*---------------------------------------------------------------*")

    replace_my_config(root_path, project_path)
    result = subprocess.run(['bash', root_path + "/testing_suites/libftest/grademe.sh",
                             "-l -s -f -n -u"], stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).stdout.decode('utf-8')
    os.rename(root_path + "/deepthought", root_path + "/.mylibftest-deepthought")
    print("Deepthought file too big. Not printed. See `.mylibftest-deepthought'.")

    with open(root_path + "/.mylibftest", 'w+') as file:
        file.write("*------------------------------------------------------*\n")
        file.write("LIBFTEST\n")
        file.write("Warning: This file contains escape sequences. Please use "
                   "`cat' to view it properly.\n")
        file.write("*------------------------------------------------------*\n")
        file.write(result)

    print(result)
    with open(root_path + "/.mylibftest", 'r') as file:
        res = ""
        for line in file:
            if "Total : " in line:
                res += line
    totals = res.split('\n')
    return totals
