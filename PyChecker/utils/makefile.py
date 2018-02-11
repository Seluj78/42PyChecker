"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import os
import glob
import subprocess


def check_makefile_clean_dir(project_path: str, binary_name: str, root_path: str):
    with open(root_path + "/.mymakefile", 'w+') as file:
        file.write("Cleaning Directory\n")
        file.write("*------------------------------------------------------*\n")
        file.write("")
        result = subprocess.run('make ' + '-C ' + project_path + ' fclean',
                                shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT).stdout.decode('utf-8')
        file.write(result + '\n')
        if os.path.exists(project_path + '/' + binary_name):
            file.write("-> Error when processing rule `fclean':"
                       " It should have removed {}\n".format(binary_name))
        if glob.glob(project_path + '*.o'):
            file.write("-> Error when processing rule `fclean':"
                       " It should have removed *.o\n")


def check_makefile_all(project_path: str, binary_name: str, root_path: str):
    makefile_path = project_path + '/Makefile'
    with open(root_path + "/.mymakefile", 'a') as file:
        file.write("*------------------------------------------------------*\n")
        file.write("Checking rule: `all'\n")
        if 'all: ' not in open(makefile_path).read():
            file.write("-> Error: rule `all' not found in the Makefile.\n")
        if 'all: $(NAME)' not in open(makefile_path).read():
            file.write("-> Error: rule `all' should call the rule `$(NAME)'\n")
        result = subprocess.run('make ' + '-C ' + project_path + ' all',
                                shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT).stdout.decode('utf-8')
        file.write(result + '\n')
        if not os.path.exists(project_path + '/' + binary_name):
            file.write("-> Error when processing rule `all':"
                       " It should have created {}\n".format(binary_name))
        if not glob.glob(project_path + '/*.o'):
            file.write("-> Error when processing rule `all':"
                       " It should NOT have removed *.o\n")
        # @todo  [ -z "$(echo ${MAKEALLTWICE} | grep -i "Nothing to be done")" -a -z "$(echo ${MAKEALLTWICE} | grep -i "is up to date")" ] && printf "%s\n" "-> Failing rule: Processing the rule 'all' twice in a row should result in nothing to be done" && RET=1


def check_makefile_clean(project_path: str, binary_name: str, root_path: str):
    makefile_path = project_path + '/Makefile'
    with open(root_path + "/.mymakefile", 'a') as file:
        file.write("*------------------------------------------------------*\n")
        file.write("Checking rule: `clean'\n")
        if 'clean: ' not in open(makefile_path).read():
            file.write("-> Error: rule `clean' not found in the Makefile.\n")
        if not os.path.exists(project_path + '/' + binary_name):
            file.write("-> Error: Cannot test rule `clean' because rule"
                       " `all' failed\n")
            # Stop the makefile test here
        result = subprocess.run('make ' + '-C ' + project_path + ' clean',
                                shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT).stdout.decode('utf-8')
        file.write(result + '\n')
        if not os.path.exists(project_path + '/' + binary_name):
            file.write("-> Error: Failing Rule: It should not have "
                       "cleaned the binary named {}.".format(binary_name))
        if glob.glob(project_path + '/*.o'):
            file.write("-> Error: Failing Rule: It should have cleaned the *.o")


def check_makefile_re(project_path: str, binary_name: str, root_path: str):
    makefile_path = project_path + '/Makefile'
    with open(root_path + "/.mymakefile", 'a') as file:
        file.write("*------------------------------------------------------*\n")
        file.write("Checking rule: `re'\n")
        if 're: ' not in open(makefile_path).read():
            file.write("-> Error: rule `re' not found in the Makefile.\n")
        if not os.path.exists(project_path + '/' + binary_name):
            file.write("-> Error: Cannot test rule `re' because rule "
                       "`all' failed\n")
        inode1 = os.stat(project_path + '/' + binary_name).st_ino
        file.write("-- Before running rule `re', the {} inode is {}\n".format(binary_name, inode1))
        result = subprocess.run('make ' + '-C ' + project_path + ' re',
                                shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT).stdout.decode('utf-8')
        file.write(result + '\n')
        inode2 = os.stat(project_path + '/' + binary_name).st_ino
        file.write("-- After running rule `re', the {} inode is {}\n".format(binary_name, inode2))
        if not glob.glob(project_path + '/*.o'):
            file.write("-> Error when processing rule `re': It should"
                       " have built the object file `*.o'\n")
        if not os.path.exists(project_path + '/' + binary_name):
            file.write("--> Error when processing rule `re': It should"
                       " have compiled a binary named {}\n".format(binary_name))
        if inode1 == inode2:
            file.write("-> Failing rule `re': It should have compiled"
                       " again the binary named {} (inode unchanged)\n".format(binary_name))


def check_makefile_fclean(project_path: str, binary_name: str, root_path: str):
    makefile_path = project_path + '/Makefile'
    with open(root_path + "/.mymakefile", 'a') as file:
        file.write("*------------------------------------------------------*\n")
        file.write("Checking rule: `fclean'\n")
        if 'fclean: ' not in open(makefile_path).read():
            file.write("-> Error: rule `fclean' not found in the Makefile.\n")
        result = subprocess.run('make ' + '-C ' + project_path + ' fclean',
                                shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT).stdout.decode('utf-8')
        file.write(result + '\n')
        if os.path.exists(project_path + '/' + binary_name):
            file.write("--> Error when processing rule `re': It should"
                       " have removed the binary named {}\n".format(binary_name))
        if glob.glob(project_path + '/*.o'):
            file.write("-> Error: Failing Rule: It should have cleaned the *.o")
        if glob.glob(project_path + '/*.a'):
            file.write("-> Error: Failing Rule: It should have cleaned the *.a")


def check_makefile_name(project_path: str, binary_name: str, root_path: str):
    makefile_path = project_path + '/Makefile'
    with open(root_path + "/.mymakefile", 'a') as file:
        file.write("*------------------------------------------------------*\n")
        file.write("Checking rule: `$(NAME)'\n")
        if '$(NAME):' not in open(makefile_path).read():
            file.write("-> Error: rule `$(NAME)' not found in the Makefile.\n")
        result = subprocess.run('make ' + '-C ' + project_path + ' ' + binary_name,
                                shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT).stdout.decode('utf-8')
        file.write(result + '\n')
        if not os.path.exists(project_path + '/' + binary_name):
            file.write("--> Error when processing rule `re': It should"
                       " have compiled a binary named {}\n".format(binary_name))
        if not glob.glob(project_path + '/*.o'):
            file.write("-> Error when processing rule `fclean': It should"
                       " NOT have removed *.o\n")
        # @todo  [ -z "$(echo ${MAKEALLTWICE} | grep -i "Nothing to be done")" -a -z "$(echo ${MAKEALLTWICE} | grep -i "is up to date")" ] && printf "%s\n" "-> Failing rule: Processing the rule 'all' twice in a row should result in nothing to be done" && RET=1


def check_makefile_phony(project_path: str, binary_name: str, root_path: str):
    makefile_path = project_path + '/Makefile'
    with open(root_path + "/.mymakefile", 'a') as file:
        file.write("*------------------------------------------------------*\n")
        file.write("Checking rule: `.PHONY'\n")
        if '.PHONY:' not in open(makefile_path).read():
            file.write("-> Error: rule `.PHONY' not found in the Makefile.\n")
        if not os.path.exists(project_path + '/' + binary_name):
            file.write("-> Error: Cannot test rule `re' because rule "
                       "`$(NAME)' failed\n")
        result = subprocess.run('make ' + '-C ' + project_path + ' .PHONY',
                                shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT).stdout.decode('utf-8')
        file.write(result + '\n')
        if not os.path.exists(project_path + '/' + binary_name):
            file.write("--> Error when processing rule `.PHONY': It should"
                       " not have cleaned the binary named {}\n".format(binary_name))
        if glob.glob(project_path + '/*.o'):
            file.write("-> Error: Failing Rule: It should have cleaned the *.o")


def check(project_path: str, binary_name: str, root_path: str):
    """
    This function is the one you call to test the makefile given with the project.

    :param project_path: The path of the project you want to test.
    :param binary_name: The binary that the makefile compiles

    :return This functions returns 1 If an error occured, 0 otherwise.
    """
    makefile_path = project_path + '/Makefile'
    if not os.path.exists(makefile_path):
        print("Error: Makefile not found.")
        return 1
    # @todo Add an error counter
    check_makefile_clean_dir(project_path, binary_name, root_path)
    check_makefile_all(project_path, binary_name, root_path)
    check_makefile_clean(project_path, binary_name, root_path)
    check_makefile_re(project_path, binary_name, root_path)
    check_makefile_fclean(project_path, binary_name, root_path)
    check_makefile_name(project_path, binary_name, root_path)
    check_makefile_phony(project_path, binary_name, root_path)
    return 0
