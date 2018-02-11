"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import os
import glob
import subprocess


def check(project_path: str, root_path: str):
    """
    This function will check the norm of the given project.

    :param project_path: The path of the project where you want to check the author file

    :return: Returns 0 if everything is ok,
     1 if there isn't any file to check,
     2 if some errors/warnings were found
    """
    files = ""
    for filename in glob.iglob(project_path + '/**/*.c', recursive=True):
        files = files + ' ' + filename
    for filename in glob.iglob(project_path + '/**/*.h', recursive=True):
        files = files + ' ' + filename
    if files == "":
        print("No source file (.c) or header (.h) to check")
        return 1
    with open(root_path + "/.mynorme", 'w+') as file:
        try:
            result = subprocess.run(['norminette'] + files.split(),
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT).stdout.decode('utf-8')
        except FileNotFoundError:
            file.write("Error: Norminette not found.\n")
        else:
            file.write(result)
            error_count = result.count('Error')
            warning_count = result.count('Warning')
            if error_count != 0 and warning_count != 0:
                print("Found {} errors and {} warnings".format(error_count,
                                                               warning_count))
                return 2
    return 0
