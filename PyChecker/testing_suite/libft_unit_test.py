"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import platform
import subprocess
import os
import io
from PyChecker.utils import git
import logging


def run(root_path: str, args):

    logging.info("Started runing `libft-unit-test` tests.")
    print("*---------------------------------------------------------------*")
    print("*------------------------libft-unit-test------------------------*")
    print("*---------------------------------------------------------------*")
    if platform.system() != 'Darwin':
        print("Sorry, this testing suite can only be ran on Darwin computers (MacOS)")
        with open(root_path + '/.mylibftunittest', 'w+') as file:
            file.write("Sorry, this testing suite can only be ran on Darwin computers (MacOS)\n")
        logging.critical("Sorry, this testing suite can only be ran on Darwin computers (MacOS)")
        return "Sorry, this testing suite can only be ran on Darwin computers (MacOS)"

    if "fatal: Not a git repository" in git.status(root_path + '/testing_suites/libft-unit-test'):
        git.clone("https://github.com/alelievr/libft-unit-test.git", root_path + '/testing_suites/libft-unit-test')
    else:
        git.reset(root_path + '/testing_suites/libft-unit-test')

    logging.debug("LUB: Opening file {}.".format(root_path + '/.mylibftunittest'))
    with open(root_path + '/.mylibftunittest', 'w+') as file:
        logging.debug("LUB: Running `make re -C {} LIBFTDIR={}`".format(root_path + '/testing_suites/libft-unit-test', args.path))
        result = subprocess.run(['make', 're', '-C', root_path + '/testing_suites/libft-unit-test', 'LIBFTDIR=' + args.path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8')
        file.write(result)
        print(result)
        logging.debug("LUB: Running `make f {} LIBFTDIR={}`".format(root_path + '/testing_suites/libft-unit-test', args.path))
        result = subprocess.run(['make', 'f', '-C', root_path + '/testing_suites/libft-unit-test', 'LIBFTDIR=' + args.path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8')
        print(result)
        file.write(result)
        logging.debug("LUB: Renaming result.log and moving it into {}".format(root_path + '/.mylibftunittest-results'))
        os.rename(root_path + '/testing_suites/libft-unit-test/result.log', root_path + '/.mylibftunittest-results')
        # Starts benchmark if asked
        if args.do_benchmark:
            logging.debug("LUB: Starting benchmark")
            oldpwd = os.getcwd()
            logging.debug("Changing directory to {}".format(root_path + '/testing_suites/libft-unit-test/'))
            os.chdir(root_path + '/testing_suites/libft-unit-test/')
            logging.debug("LUB: Running `./run_test -b`")
            result = subprocess.run(['./run_test', '-b'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8')
            logging.debug("LUB: Changing back directory to {}".format(oldpwd))
            os.chdir(oldpwd)
            print(result)
            file.write(result)
            logging.debug("LUB: Opening file {}".format(root_path + '/.mylibftunittest'))
            with open(root_path + '/.mylibftunittest', 'r') as file2:
                for line in file2:
                    if "WINNER:" in line:
                        benchmark_results = line
    # Open result file with correct encoding
    logging.debug("LUB: Opening file {} with encoding ISO-8859-1".format(root_path + '/.mylibftunittest-results'))
    with io.open(root_path + '/.mylibftunittest-results', "r", encoding="ISO-8859-1") as file:
        data = file.read()
        results = 'OKs: ' + str(data.count('OK')) + '\n'
        results += 'KOs: ' + str(data.count('KO')) + '\n'
        results += 'FAILED: ' + str(data.count('FAILED')) + '\n'
        results += 'NO CRASH: ' + str(data.count('NO CRASH')) + '\n'
        results += 'protected: ' + str(data.count('protected')) + '\n'
        results += 'not protected:' + str(data.count('not protected'))
    print(results)
    # Send results back
    logging.info("Finished runing `libft-unit-test` tests.")
    if args.do_benchmark:
        return results, benchmark_results
    else:
        return results
