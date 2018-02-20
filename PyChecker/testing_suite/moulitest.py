"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import os
import subprocess
from PyChecker.utils import git
import logging

def include_libft_bonuses(root_path: str):
    """
    This function removes the `.exclude` extention to the libft bonuses files.
    """
    logging.info("MOULITEST: Removing `.exclude` to bonuses files")
    moulitest_libft_tests_path = root_path + "/testing_suites/moulitest/libft_tests/tests"
    files = os.listdir(moulitest_libft_tests_path)
    for file in files:
        if file[:2] == "02":
            if file.endswith(".exclude"):
                logging.debug("MOULITEST: Now processing {}".format(file))
                os.rename(os.path.join(moulitest_libft_tests_path, file),
                          os.path.join(moulitest_libft_tests_path, file[:-8]))


def exclude_libft_bonuses(root_path: str):
    """
    This function Adds the `.exclude` extention to the libft bonuses files.
    """
    logging.info("MOULITEST: Adding `.exclude` to bonuses files")
    moulitest_libft_tests_path = root_path + "/testing_suites/moulitest/libft_tests/tests"
    files = os.listdir(moulitest_libft_tests_path)
    for file in files:
        if file[:2] == "02":
            logging.debug("MOULITEST: Now processing {}".format(file))
            os.rename(os.path.join(moulitest_libft_tests_path, file),
                      os.path.join(moulitest_libft_tests_path, file + '.exclude'))


def execute_test(test_name: str, root_path: str):
    available_tests = ['libft_part1', 'libft_part2', 'libft_bonus',
                       'get_next_line', 'gnl', 'ft_ls', 'ft_printf']
    if test_name not in available_tests:
        logging.error("Given test not in moulitest available tests.")
        raise ValueError("Given test not in moulitest available tests.")
    logging.debug("MOULITEST: Opening file {}.".format(root_path + "/.mymoulitest"))
    with open(root_path + "/.mymoulitest", 'w+') as file:
        file.write("*------------------------------------------------------*\n")
        file.write("MOULITEST\n")
        file.write("Warning: This file contains escape sequences. Please use"
                   " `cat' to view it properly.\n")
        file.write("*------------------------------------------------------*\n")
        # Run moulitest
        logging.debug("MOULITEST: Running `make {} -C {}`".format(test_name, root_path + '/testing_suites/moulitest'))
        result = subprocess.run('make ' + test_name + ' -C ' + root_path +
                                '/testing_suites/moulitest', shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT).stdout.decode('utf-8')
        file.write(result + '\n')
        print(result)
    # Parse the result
    logging.debug("MOULITEST: Opening file {}".format(root_path + "/.mymoulitest"))
    with open(root_path + "/.mymoulitest", 'r') as file:
        for line in file:
            if "(dots)." in line:
                logging.debug("Found string `(dots).`")
                line = line[12:-13]
                return line


def run(project_path: str, has_libft_bonuses: bool, project: str, root_path: str):
    logging.info("Started moulitest")
    if "fatal: Not a git repository" in git.status(root_path + '/testing_suites/moulitest'):
        git.clone("https://github.com/yyang42/moulitest.git", root_path + '/testing_suites/moulitest')
    else:
        git.reset(root_path + '/testing_suites/moulitest')

    print("*---------------------------------------------------------------*")
    print("*--------------------------Moulitest----------------------------*")
    print("*---------------------------------------------------------------*")
    available_projects = ['ft_ls', 'ft_printf', 'gnl', 'libft', 'libftasm']
    #  Available projects checks if the given project corresponds to one the moulitest tests.
    if project not in available_projects:
        logging.error("Given project not in moulitest available projects.")
        raise ValueError("Given project not in moulitest available projects.")

    if project == "libft":
        logging.info("MOULITEST: starting tests for `libft`")
        logging.debug("MOULITEST: Opening file {}".format(root_path + "/testing_suites/moulitest/config.ini"))
        with open(root_path + "/testing_suites/moulitest/config.ini", 'w+') as file:
            file.write("LIBFT_PATH = " + project_path)
        include_libft_bonuses(root_path)
        # @todo: Fix moulitest makefile (it starts the bonus even when not asked.)
        if not has_libft_bonuses:
            exclude_libft_bonuses(root_path)
            results = execute_test("libft_bonus", root_path)
            include_libft_bonuses(root_path)
        else:
            results = execute_test("libft_bonus", root_path)
    logging.info("Finished moulitest")
    return results
