"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import os
import subprocess


def run(project_path: str, root_path: str):
    """
    This function runs the libftest to the given project.

    :param project_path: The path of the project you want to test.
    """
    print("*---------------------------------------------------------------*")
    print("*----------------------------Libftest---------------------------*")
    print("*---------------------------------------------------------------*")
    try:
        open("testing_suites/libftest/my_config.sh", 'r')
    except FileNotFoundError:
        subprocess.run(['bash', "testing_suites/libftest/grademe.sh"])
    with open('testing_suites/libftest/my_config.sh', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace('PATH_LIBFT=~/libft', "PATH_LIBFT=" + project_path)
    filedata = filedata.replace('PATH_DEEPTHOUGHT=${PATH_TEST}',
                                "PATH_DEEPTHOUGHT=" + root_path)
    with open('testing_suites/libftest/my_config.sh', 'w') as file:
        file.write(filedata)
    # @todo Parse libftest output for UI and parse score for display and return values.
    result = subprocess.run(['bash', "testing_suites/libftest/grademe.sh",
                             "-l -s -f -n -u"], stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).stdout.decode('utf-8')
    os.rename("deepthought", ".mylibftest-deepthought")
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
    totals = []
    totals = res.split('\n')
    return totals
