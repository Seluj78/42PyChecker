"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import os
import subprocess

def include_libft_bonuses(root_path: str):
    """
    This method removes the `.exclude` extention to the libft bonuses files.
    """
    moulitest_libft_tests_path = root_path + "/testing_suites/moulitest/libft_tests/tests"
    files = os.listdir(moulitest_libft_tests_path)
    for file in files:
        if file[:2] == "02":
            if file.endswith(".exclude"):
                os.rename(os.path.join(moulitest_libft_tests_path, file),
                          os.path.join(moulitest_libft_tests_path, file[:-8]))


def exclude_libft_bonuses(root_path: str):
    """
    This method Adds the `.exclude` extention to the libft bonuses files.
    """
    moulitest_libft_tests_path = root_path + "/testing_suites/moulitest/libft_tests/tests"
    files = os.listdir(moulitest_libft_tests_path)
    for file in files:
        if file[:2] == "02":
            os.rename(os.path.join(moulitest_libft_tests_path, file),
                      os.path.join(moulitest_libft_tests_path, file + '.exclude'))


def execute_test(test_name: str, root_path: str):
    # @todo add a protection if test_name isn't compatible with the current project and if not in list of available test for moulitest
    with open(root_path + "/.mymoulitest", 'w+') as file:
        file.write("*------------------------------------------------------*\n")
        file.write("MOULITEST\n")
        file.write("Warning: This file contains escape sequences. Please use"
                   " `cat' to view it properly.\n")
        file.write("*------------------------------------------------------*\n")
        # @todo Get the result line of moulitest and parse it.
        result = subprocess.run('make ' + test_name + ' -C ' + root_path +
                                '/testing_suites/moulitest', shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT).stdout.decode('utf-8')
        file.write(result + '\n')
        print(result)
    with open(root_path + "/.mymoulitest", 'r') as file:
        for line in file:
            if "(dots)." in line:
                line = line[12:-13]
                return line


def run(project_path: str, has_libft_bonuses: bool, project: str, root_path: str):
    print("*---------------------------------------------------------------*")
    print("*--------------------------Moulitest----------------------------*")
    print("*---------------------------------------------------------------*")
    available_projects = ['ft_ls', 'ft_printf', 'gnl', 'libft', 'libftasm']
    #  Available projects checks if the given project corresponds to one the moulitest tests.
    if project not in available_projects:
        raise ValueError("given project not in moulitest available projects.")
    if project == "libft":
        with open(root_path + "/testing_suites/moulitest/config.ini", 'w+') as file:
            file.write("LIBFT_PATH = " + project_path)
        include_libft_bonuses(root_path)
        # @todo Fix moulitest makefile (it starts the bonus even when not asked.)
        if not has_libft_bonuses:
            exclude_libft_bonuses(root_path)
            results = execute_test("libft_bonus", root_path)
            include_libft_bonuses(root_path)
        else:
            results = execute_test("libft_bonus", root_path)
    return results
