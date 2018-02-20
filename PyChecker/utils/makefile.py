"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import os
import re
import glob
import subprocess
import logging


def check_makefile_clean_dir(project_path: str, binary_name: str, root_path: str):
    """
    This function will clean the project's directory and test if the binary
    and the .o were removed.

    :param project_path: The project path where what needs to be tested is.
    :param binary_name: The name of the binary the makefile will compile
    :param root_path: The absolute path leading to the script's main file.

    :return: Returns the number of errors encountered during that function.
    """
    error_count = 0
    logging.debug("MAKEFILE: Starting Makefile dir cleaning")
    with open(root_path + "/.mymakefile", 'w+') as file:
        logging.debug("MAKEFILE: Opening file {}.".format(root_path + "/.mymakefile"))
        file.write("Cleaning Directory\n")
        print("Cleaning Directory")
        file.write("*------------------------------------------------------*\n")
        file.write("")
        # Run make fclean in the project's directory
        logging.debug("MAKEFIlE: Running `make -C {} fclean`".format(project_path))
        result = subprocess.run('make ' + '-C ' + project_path + ' fclean',
                                shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT).stdout.decode('utf-8')
        file.write(result + '\n')
        print(result)
        # If the binary or the object file still exists after the fclean,
        # print an error and increment the error counter.
        if os.path.exists(project_path + '/' + binary_name):
            logging.error("MAKEFILE: Error when processing rule `fclean':"
                       " It should have removed {}\n".format(binary_name))
            file.write("-> Error when processing rule `fclean':"
                       " It should have removed {}\n".format(binary_name))
            print("-> Error when processing rule `fclean':"
                       " It should have removed {}".format(binary_name))
            error_count += 1
        if glob.glob(project_path + '*.o'):
            logging.error("MAKEFILE: Error when processing rule `fclean':"
                       " It should have removed *.o\n")
            file.write("-> Error when processing rule `fclean':"
                       " It should have removed *.o\n")
            print("-> Error when processing rule `fclean':"
                       " It should have removed *.o")
            error_count += 1
    logging.debug("MAKEFILE: Finished dir cleaning")
    return error_count


def check_makefile_all(project_path: str, binary_name: str, root_path: str):
    """
    This function will check the rule `all` for the makefile of the given project.

    :param project_path: The project path where what needs to be tested is.
    :param binary_name: The name of the binary the makefile will compile
    :param root_path: The absolute path leading to the script's main file.

    :return: Returns the number of errors encountered during that function.
    """
    logging.debug("MAKEFILE: Starting Makefile `all` check.")
    error_count = 0
    makefile_path = project_path + '/Makefile'
    match = False
    logging.debug("MAKEFILE: Opening file {}.".format(makefile_path))
    with open(makefile_path, 'r') as makefile:
        logging.debug("MAKEFILE: Opening file {}.".format(root_path + "/.mymakefile"))
        with open(root_path + "/.mymakefile", 'a') as file:
            file.write("*------------------------------------------------------*\n")
            file.write("Checking rule: `all'\n")
            print("Checking rule: `all'")
            # Searches every line of the makefile for the string `all`
            # followed by spaces and/or tabs and then a `:`
            logging.debug("MAKEFILE: Searching through the Makefile line by line for the rule `all`")
            for line in makefile:
                if re.match('^all[\t ]*:', line):
                    logging.debug("MAKEFILE: Regex found rule all.")
                    match = True
                    break
            if not match:
                logging.error("MAKEFILE: Error: rule `all' not found in the Makefile.")
                file.write("-> Error: rule `all' not found in the Makefile.\n")
                print("-> Error: rule `all' not found in the Makefile.")
                error_count += 1
                logging.debug("MAKEFILE: Finishing Makefile `all` check.")
                return error_count
            # Searches every line of the makefile for the string `all` followed
            # by tabs and/or spaces and then `:` then tabs and spaces again and
            # then for the string `$(NAME)`
            logging.debug("MAKEFILE: Searching through the Makefile line by line for the rule `all` followed by `$(NAME)`")
            for line in makefile:
                if re.match('^all[\t ]*:[\t ]*\$\(NAME\)', line):
                    logging.debug("MAKEFILE: Regex found rule all followed by `$(NAME)`.")
                    match = True
                    break
            if not match:
                logging.error("MAKEFILE: Error: rule `all' should call the rule `$(NAME)'")
                file.write("-> Error: rule `all' should call the rule `$(NAME)'\n")
                print("-> Error: rule `all' should call the rule `$(NAME)'")
                error_count += 1
                logging.debug("MAKEFILE: Finishing Makefile `all` check.")
                return error_count
            # Runs make all in the project's directory
            logging.debug("MAKEFILE: Running `make -C {} all`".format(project_path))
            result = subprocess.run('make ' + '-C ' + project_path + ' all',
                                    shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT).stdout.decode('utf-8')
            file.write(result + '\n')
            print(result)
            # Checks if binary and object file were created.
            if not os.path.exists(project_path + '/' + binary_name):
                logging.error("MAKEFILE: Error when processing rule `all':"
                           " It should have created {}\n".format(binary_name))
                file.write("-> Error when processing rule `all':"
                           " It should have created {}\n".format(binary_name))
                print("-> Error when processing rule `all':"
                           " It should have created {}".format(binary_name))
                error_count += 1
            if not glob.glob(project_path + '/*.o'):
                logging.error("MAKEFILE: Error when processing rule `all':"
                           " It should NOT have removed *.o\n")
                file.write("-> Error when processing rule `all':"
                           " It should NOT have removed *.o\n")
                print("-> Error when processing rule `all':"
                           " It should NOT have removed *.o")
                error_count += 1
            # @todo: [ -z "$(echo ${MAKEALLTWICE} | grep -i "Nothing to be done")" -a -z "$(echo ${MAKEALLTWICE} | grep -i "is up to date")" ] && printf "%s\n" "-> Failing rule: Processing the rule 'all' twice in a row should result in nothing to be done" && RET=1
    logging.debug("MAKEFILE: Finishing Makefile `all` check.")
    return error_count


def check_makefile_clean(project_path: str, binary_name: str, root_path: str):
    """
    This function will check the rule `clean` for the makefile of the given project.

    :param project_path: The project path where what needs to be tested is.
    :param binary_name: The name of the binary the makefile will compile
    :param root_path: The absolute path leading to the script's main file.

    :return: Returns the number of errors encountered during that function.
    """
    logging.debug("MAKEFILE: Starting Makefile `clean` check.")
    error_count = 0
    makefile_path = project_path + '/Makefile'
    match = False
    logging.debug("MAKEFILE: Opening file {}.".format(makefile_path))
    with open(makefile_path, 'r') as makefile:
        logging.debug("MAKEFILE: Opening file {}.".format(root_path + "/.mymakefile"))
        with open(root_path + "/.mymakefile", 'a') as file:
            file.write("*------------------------------------------------------*\n")
            file.write("Checking rule: `clean'\n")
            print("Checking rule: `clean'")
            # Searches every line of the makefile for the string `clean`
            # followed by `:`
            logging.debug("MAKEFILE: Searching through the Makefile line by line for the rule `clean`")
            for line in makefile:
                if re.match('^clean[\t ]*:', line):
                    logging.debug("MAKEFILE: Regex found rule `clean`.")
                    match = True
                    break
            if not match:
                logging.error("MAKEFILE: Error: rule `fclean' not found in the Makefile")
                file.write("-> Error: rule `clean' not found in the Makefile.\n")
                print("-> Error: rule `clean' not found in the Makefile.")
                error_count += 1
                logging.debug("MAKEFILE: Finished Makefile `clean` check.")
                return error_count
            # If previous rule failed, print an error message, increment error
            # counter and return number of errors.
            if not os.path.exists(project_path + '/' + binary_name):
                logging.error("MAKEFILE: Error: Cannot test rule `clean' because rule"
                           " `all' failed")
                file.write("-> Error: Cannot test rule `clean' because rule"
                           " `all' failed\n")
                print("-> Error: Cannot test rule `clean' because rule"
                           " `all' failed")
                error_count += 1
                logging.debug("MAKEFILE: Finished Makefile `clean` check.")
                return error_count
            # Run `make clean` in the project's directory
            logging.debug("MAKEFILE: Running `make -C {} clean`".format(project_path))
            result = subprocess.run('make ' + '-C ' + project_path + ' clean',
                                    shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT).stdout.decode('utf-8')
            file.write(result + '\n')
            print(result)
            # If the binary name is not here and/or the object files are here,
            # the rule failed.
            if not os.path.exists(project_path + '/' + binary_name):
                logging.error("MAKEFILE: Error: Failing Rule: It should not have "
                           "cleaned the binary named {}.".format(binary_name))
                file.write("-> Error: Failing Rule: It should not have "
                           "cleaned the binary named {}.\n".format(binary_name))
                print("-> Error: Failing Rule: It should not have "
                           "cleaned the binary named {}.".format(binary_name))
                error_count += 1
            if glob.glob(project_path + '/*.o'):
                logging.error("MAKEFILE: Error: Failing Rule: It should have cleaned the *.o")
                file.write("-> Error: Failing Rule: It should have cleaned the *.o\n")
                print("-> Error: Failing Rule: It should have cleaned the *.o")
                error_count += 1
    logging.debug("MAKEFILE: Finished Makefile `clean` check.")
    return error_count


def check_makefile_re(project_path: str, binary_name: str, root_path: str):
    """
    This function will check the rule `re` for the makefile of the given project.

    :param project_path: The project path where what needs to be tested is.
    :param binary_name: The name of the binary the makefile will compile
    :param root_path: The absolute path leading to the script's main file.

    :return: Returns the number of errors encountered during that function.
    """
    logging.debug("MAKEFILE: Starting Makefile `re` check.")
    error_count = 0
    makefile_path = project_path + '/Makefile'
    match = False
    logging.debug("MAKEFILE: Opening file {}.".format(makefile_path))
    with open(makefile_path, 'r') as makefile:
        logging.debug("MAKEFILE: Opening file {}.".format(root_path + "/.mymakefile"))
        with open(root_path + "/.mymakefile", 'a') as file:
            file.write("*------------------------------------------------------*\n")
            file.write("Checking rule: `re'\n")
            print("Checking rule: `re'\n")
            logging.debug("MAKEFILE: Searching through the Makefile line by line for the rule `re`")
            for line in makefile:
                if re.match('^re[\t ]*:', line):
                    logging.debug("MAKEFILE: Regex found rule `re`.")
                    match = True
                    break
            if not match:
                logging.error("MAKEFILE: Error: rule `re' not found in the Makefile")
                file.write("-> Error: rule `re' not found in the Makefile.\n")
                print("-> Error: rule `re' not found in the Makefile.")
                error_count += 1
                logging.error("MAKEFILE: Finished Makefile `re` check.")
                return error_count
            if not os.path.exists(project_path + '/' + binary_name):
                logging.error("MAKEFILE: Error: Cannot test rule `re' because rule"
                           " `all' failed")
                file.write("-> Error: Cannot test rule `re' because rule "
                           "`all' failed\n")
                print("-> Error: Cannot test rule `re' because rule "
                           "`all' failed")
                error_count += 1
                logging.error("MAKEFILE: Finished Makefile `re` check.")
                return error_count
            inode1 = os.stat(project_path + '/' + binary_name).st_ino
            logging.debug("MAKEFILE: Before running rule `re', the {} inode is {}".format(binary_name, inode1))
            file.write("-- Before running rule `re', the {} inode is {}\n".format(binary_name, inode1))
            print("-- Before running rule `re', the {} inode is {}".format(binary_name, inode1))
            logging.debug("MAKEFILE: Running `make -C {} re".format(project_path))
            result = subprocess.run('make ' + '-C ' + project_path + ' re',
                                    shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT).stdout.decode('utf-8')
            file.write(result + '\n')
            print(result)
            inode2 = os.stat(project_path + '/' + binary_name).st_ino
            logging.debug("MAKEFILE: After running rule `re', the {} inode is {}".format(binary_name, inode2))
            file.write("-- After running rule `re', the {} inode is {}\n".format(binary_name, inode2))
            print("-- After running rule `re', the {} inode is {}".format(binary_name, inode2))
            if not glob.glob(project_path + '/*.o'):
                logging.error("MAKEFILE: Error when processing rule `re': It should"
                           " have built the object file `*.o'")
                file.write("-> Error when processing rule `re': It should"
                           " have built the object file `*.o'\n")
                print("-> Error when processing rule `re': It should"
                           " have built the object file `*.o'")
                error_count += 1
            if not os.path.exists(project_path + '/' + binary_name):
                logging.error("MAKEFILE: Error when processing rule `re': It should"
                           " have compiled a binary named {}".format(binary_name))
                file.write("--> Error when processing rule `re': It should"
                           " have compiled a binary named {}\n".format(binary_name))
                print("--> Error when processing rule `re': It should"
                           " have compiled a binary named {}".format(binary_name))
                error_count += 1
            if inode1 == inode2:
                logging.error("MAKEFILE: Failing rule `re': It should have compiled"
                           " again the binary named {} (inode unchanged)".format(binary_name))
                file.write("-> Failing rule `re': It should have compiled"
                           " again the binary named {} (inode unchanged)\n".format(binary_name))
                print("-> Failing rule `re': It should have compiled"
                           " again the binary named {} (inode unchanged)".format(binary_name))
                error_count += 1
    logging.error("MAKEFILE: Finished Makefile `re` check.")
    return error_count


def check_makefile_fclean(project_path: str, binary_name: str, root_path: str):
    """
    This function will check the rule `fclean` for the makefile of the given project.

    :param project_path: The project path where what needs to be tested is.
    :param binary_name: The name of the binary the makefile will compile
    :param root_path: The absolute path leading to the script's main file.

    :return: Returns the number of errors encountered during that function.
    """
    logging.debug("MAKEFILE: Starting Makefile `fclean` check.")
    error_count = 0
    makefile_path = project_path + '/Makefile'
    match = False
    logging.debug("MAKEFILE: Opening file {}.".format(makefile_path))
    with open(makefile_path, 'r') as makefile:
        logging.debug("MAKEFILE: Opening file {}.".format(root_path + "/.mymakefile"))
        with open(root_path + "/.mymakefile", 'a') as file:
            file.write("*------------------------------------------------------*\n")
            file.write("Checking rule: `fclean'\n")
            print("Checking rule: `fclean'\n")
            logging.debug("MAKEFILE: Searching through the Makefile line by line for the rule `fclean`")
            # @todo: Fix for loop, add a break at first match for makefile check `fclean`
            for line in makefile:
                logging.debug("MAKEFILE: Regex found rule `fclean`.")
                if re.match('^fclean[\t ]*:', line):
                    match = True
                    break
            if not match:
                logging.error("MAKEFILE: Error: rule `fclean' not found in the Makefile")
                file.write("-> Error: rule `fclean' not found in the Makefile.\n")
                print("-> Error: rule `fclean' not found in the Makefile.")
                error_count += 1
                logging.error("MAKEFILE: Finished Makefile `fclean` check.")
                return error_count
            logging.debug("MAKEFILE: Running `make -C {} fclean`".format(project_path))
            result = subprocess.run('make ' + '-C ' + project_path + ' fclean',
                                    shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT).stdout.decode('utf-8')
            file.write(result + '\n')
            print(result)
            if os.path.exists(project_path + '/' + binary_name):
                logging.error("MAKEFILE: Error when processing rule `re': It should"
                    " have compiled a binary named {}".format(binary_name))
                file.write("--> Error when processing rule `re': It should"
                           " have removed the binary named {}\n".format(binary_name))
                print("--> Error when processing rule `re': It should"
                           " have removed the binary named {}".format(binary_name))
                error_count += 1
            if glob.glob(project_path + '/*.o'):
                logging.error("MAKEFILE: Error when processing rule `re': It should"
                           " have built the object file `*.o'")
                file.write("-> Error: Failing Rule: It should have cleaned the *.o\n")
                print("-> Error: Failing Rule: It should have cleaned the *.o")
                error_count += 1
            if glob.glob(project_path + '/*.a'):
                logging.error("MAKEFILE: Error: Failing Rule: It should have cleaned the *.a")
                file.write("-> Error: Failing Rule: It should have cleaned the *.a\n")
                print("-> Error: Failing Rule: It should have cleaned the *.a")
                error_count += 1
    logging.error("MAKEFILE: Finished Makefile `fclean` check.")
    return error_count


def check_makefile_name(project_path: str, binary_name: str, root_path: str):
    """
    This function will check the rule `$(NAME)` for the makefile of the given project.

    :param project_path: The project path where what needs to be tested is.
    :param binary_name: The name of the binary the makefile will compile
    :param root_path: The absolute path leading to the script's main file.

    :return: Returns the number of errors encountered during that function.
    """
    logging.debug("MAKEFILE: Starting Makefile `$(NAME)` check.")
    error_count = 0
    makefile_path = project_path + '/Makefile'
    match = False
    logging.debug("MAKEFILE: Opening file {}.".format(makefile_path))
    with open(makefile_path, 'r') as makefile:
        logging.debug("MAKEFILE: Opening file {}.".format(root_path + "/.mymakefile"))
        with open(root_path + "/.mymakefile", 'a') as file:
            file.write("*------------------------------------------------------*\n")
            file.write("Checking rule: `$(NAME)'\n")
            print("Checking rule: `$(NAME)'")
            logging.debug("MAKEFILE: Searching through the Makefile line by line for the rule `$(NAME)`")
            for line in makefile:
                if re.match('^\$\(NAME\)[\t ]*:', line):
                    logging.debug("MAKEFILE: Regex found rule `$(NAME)`.")
                    match = True
                    break
            if not match:
                logging.error("MAKEFILE: Error: rule `$(NAME)' not found in the Makefile")
                file.write("-> Error: rule `$(NAME)' not found in the Makefile.\n")
                print("-> Error: rule `$(NAME)' not found in the Makefile.")
                error_count += 1
                logging.debug("MAKEFILE: Finished Makefile `$(NAME)` check.")
                return error_count
            logging.debug("MAKEFILE: Running `make -C {} {}`".format(project_path, binary_name))
            result = subprocess.run('make ' + '-C ' + project_path + ' ' + binary_name,
                                    shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT).stdout.decode('utf-8')
            file.write(result + '\n')
            print(result)
            if not os.path.exists(project_path + '/' + binary_name):
                logging.error("MAKEFILE: Error when processing rule `$(NAME)': It should"
                           " have compiled a binary named {}".format(binary_name))
                file.write("--> Error when processing rule `re': It should"
                           " have compiled a binary named {}\n".format(binary_name))
                print("--> Error when processing rule `re': It should"
                           " have compiled a binary named {}".format(binary_name))
                error_count += 1
            if not glob.glob(project_path + '/*.o'):
                logging.error("-> Error when processing rule `fclean': It should"
                           " NOT have removed *.o")
                file.write("-> Error when processing rule `fclean': It should"
                           " NOT have removed *.o\n")
                print("-> Error when processing rule `fclean': It should"
                           " NOT have removed *.o\n")
                error_count += 1
            # @todo: [ -z "$(echo ${MAKEALLTWICE} | grep -i "Nothing to be done")" -a -z "$(echo ${MAKEALLTWICE} | grep -i "is up to date")" ] && printf "%s\n" "-> Failing rule: Processing the rule 'all' twice in a row should result in nothing to be done" && RET=1
    logging.debug("MAKEFILE: Finished Makefile `$(NAME)` check.")
    return error_count


def check_makefile_phony(project_path: str, binary_name: str, root_path: str):
    """
    This function will check the rule `.PHONY` for the makefile of the given project.

    :param project_path: The project path where what needs to be tested is.
    :param binary_name: The name of the binary the makefile will compile
    :param root_path: The absolute path leading to the script's main file.

    :return: Returns the number of errors encountered during that function.
    """
    logging.debug("MAKEFILE: Starting Makefile `.PHONY` check")
    error_count = 0
    makefile_path = project_path + '/Makefile'
    match = False
    logging.debug("MAKEFILE: Opening file {}.".format(makefile_path))
    with open(makefile_path, 'r') as makefile:
        logging.debug("MAKEFILE: Opening file {}.".format(root_path + "/.mymakefile"))
        with open(root_path + "/.mymakefile", 'a') as file:
            file.write("*------------------------------------------------------*\n")
            file.write("Checking rule: `.PHONY'\n")
            print("Checking rule: .PHONY")
            logging.debug("MAKEFILE: Searching through the Makefile line by line for the rule `.PHONY`")
            for line in makefile:
                if re.match('^\.PHONY[\t ]*:', line):
                    logging.debug("MAKEFILE: Regex found rule `.PHONY`.")
                    match = True
                    break
            if not match:
                logging.error("MAKEFILE: Error: rule `.PHONY' not found in the Makefile")
                file.write("-> Error: rule `.PHONY' not found in the Makefile.\n")
                print("-> Error: rule `.PHONY' not found in the Makefile.")
                error_count += 1
                logging.debug("MAKEFILE: Finished Makefile `.PHONY` check.")
                return error_count
            if not os.path.exists(project_path + '/' + binary_name):
                logging.error("MAKEFILE: Error: Cannot test rule `.PHONY' because rule "
                           "`$(NAME)' failed")
                file.write("-> Error: Cannot test rule `.PHONY' because rule "
                           "`$(NAME)' failed\n")
                print("-> Error: Cannot test rule `.PHONY' because rule "
                           "`$(NAME)' failed")
                error_count += 1
                return error_count
            logging.debug("MAKEFILE: Running `make -C {} .PHONY`".format(project_path))
            result = subprocess.run('make ' + '-C ' + project_path + ' .PHONY',
                                    shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT).stdout.decode('utf-8')
            file.write(result + '\n')
            print(result)
            if not os.path.exists(project_path + '/' + binary_name):
                logging.error("MAKEFILE: Error when processing rule `.PHONY': It should"
                           " not have cleaned the binary named {}".format(binary_name))
                file.write("--> Error when processing rule `.PHONY': It should"
                           " not have cleaned the binary named {}\n".format(binary_name))
                print("--> Error when processing rule `.PHONY': It should"
                           " not have cleaned the binary named {}\n".format(binary_name))
                error_count += 1
            if glob.glob(project_path + '/*.o'):
                logging.error("MAKEFILE: Error: Failing Rule: It should have cleaned the *.o")
                file.write("-> Error: Failing Rule: It should have cleaned the *.o\n")
                print("-> Error: Failing Rule: It should have cleaned the *.o")
                error_count += 1
    logging.debug("MAKEFILE: Finished Makefile `.PHONY` check.")
    return error_count


def check(project_path: str, root_path: str):
    """
    This function will run all the makefile checks.

    :param project_path: The path of the project you want to test.
    :param binary_name: The binary that the makefile compiles
    :param root_path: The absolute path leading to the script's main file.

    :return This functions returns the number of errors found on the makefile
    """
    logging.info("Starting Makefile Check")
    print("*---------------------------------------------------------------*")
    print("*----------------------------Makefile---------------------------*")
    print("*---------------------------------------------------------------*")

    makefile_path = project_path + '/Makefile'
    logging.info("MAKEFILE: Makefile path should be {}.".format(makefile_path))
    if not os.path.exists(makefile_path):
        logging.error("MAKEFILE: Error: Makefile not found at `{}`.".format(makefile_path))
        print("--> Error: Makefile not found.")
        return "--> Error: Makefile not found."
    with open(makefile_path, 'r') as file:
        logging.debug("MAKEFILE: Opening file {}.".format(makefile_path))
        data = file.read()
        binary_name = re.findall("NAME[\s]*=[\s]*(.*)", data)[0]
        logging.debug("MAKEFIlE: Reading file and found binary name `{}`.".format(binary_name))

    error_count = 0
    logging.info("MAKEFILE: Starting Makefile rules check.")
    error_count += check_makefile_clean_dir(project_path, binary_name, root_path)
    error_count += check_makefile_all(project_path, binary_name, root_path)
    error_count += check_makefile_clean(project_path, binary_name, root_path)
    error_count += check_makefile_re(project_path, binary_name, root_path)
    error_count += check_makefile_fclean(project_path, binary_name, root_path)
    error_count += check_makefile_name(project_path, binary_name, root_path)
    error_count += check_makefile_phony(project_path, binary_name, root_path)
    logging.info("MAKEFILE: Finished Makefile rules check.")

    print("\n\n\t\tFound {} errors on your makefile".format(error_count))
    with open(root_path + "/.mymakefile", 'a') as file:
        logging.debug("MAKEFILE: Opening file {}.".format(root_path + "/.mymakefile"))
        file.write("\n\n\t\tFound {} errors on your makefile\n".format(error_count))
    logging.debug("MAKEFILE: Found {} errors on your makefile".format(error_count))
    logging.info("Finished Makefile Check")
    return "Found {} errors on your makefile".format(error_count)
