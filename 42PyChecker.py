import os
import sys
import glob
import subprocess
import re

def check_author_file(project_path: str):
    """
    :param project_path: The path of the project where you want to check the author file

    :return: This function will return 0 if everything is ok,
     1 if file not found,
     2 if there's too many lines in the file,
     3 if the newline char is missing in the end of line
    """
    # @todo: Add a skip if author file set as optional
    author_fr = project_path + "/auteur"
    author_us = project_path + "/author"
    if os.path.exists(author_fr):
        count = len(open(author_fr).readlines())
        author = "fr"
    elif os.path.exists(author_us):
        count = len(open(author_us).readlines())
        author = "us"
    else:
        print("Author file not found")
        return 1  # @todo Add message if author file is set as optional
    if count != 1:
        print("Too many lines in author file (Or the file is empty)")
        return 2  # @todo Add message if author file is set as optional or if project isn't solo
    if author == "fr":
        with open(author_fr, 'r') as file:
            content = file.read()
            if "\n" not in content:
                print("Missing <newline> character at the end of line")
                return 3  # @todo: Add message if author file is set as optional and handle multiple authors
    elif author == "us":
        with open(author_us, 'r') as file:
            content = file.read()
            if "\n" not in content:
                print("Missing <newline> character at the end of line")
                return 3  # @todo: Add message if author file is set as optional and handle multiple authors
    return 0


def check_norme(project_path: str):
    """
    :param project_path: The path of the project where you want to check the author file

    :return: Returns 0 if everything is ok,
     1 if there isn't any file to check,
     2 if some errors/warnings were found
    """
    # @todo: Add a skip if norme is set as optional
    files = ""
    for filename in glob.iglob(project_path + '/**/*.c', recursive=True):
        files = files + ' ' + filename
    for filename in glob.iglob(project_path + '/**/*.h', recursive=True):
        files = files + ' ' + filename
    if files == "":
        print("No source file (.c) or header (.h) to check")
        return 1
    with open(os.path.dirname(os.path.realpath(__file__)) + "/.mynorme", 'w+') as file:
        result = subprocess.run(['norminette'] + files.split(), stdout=subprocess.PIPE).stdout.decode('utf-8')
        file.write(result)
    error_count = result.count('Error')
    warning_count = result.count('Warning')
    if error_count != 0 and warning_count != 0:
        print("Found {} errors and {} warnings".format(error_count, warning_count))
        return 2
    print("Normed passed")
    return 0


def check_makefile(project_path: str, binary_name: str):
    """
    :param project_path: The path of the project
    :param binary_name: The binary that the makefile makes

    :return: Returns 0 if makefile ok,
     1 if the makefile doesnt exists
     2 if the binary wasn't removed
     3 if the .o files weren't removed
    """
    # @todo: Split check_makefile in separate methods for each rule
    makefile_path = project_path + '/Makefile'
    if not os.path.exists(makefile_path):
        print("Error: Makefile not found.")
        return 1
    with open(os.path.dirname(os.path.realpath(__file__)) + "/.mymakefile", 'w+') as file:
        file.write("Cleaning Directory\n")
        file.write("*------------------------------------------------------*\n")
        file.write("")
        result = subprocess.run('make ' + '-C ' + project_path + ' fclean', shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
        file.write(result + '\n')
        if os.path.exists(project_path + '/' + binary_name):
            file.write("-> Error when processing rule `fclean': It should have removed {}\n".format(binary_name))
            #return 2 @todo: Here it doesnt return, it will just add more errors to the error counter
        if glob.glob(project_path + '*.o'):
            file.write("-> Error when processing rule `fclean': It should have removed *.o\n")
            #return 3
        file.write("*------------------------------------------------------*\n")
        file.write("Checking rule: `all'\n")
        if 'all: ' not in open(makefile_path).read():
            file.write("-> Error: rule `all' not found in the Makefile.\n")
        if 'all: $(NAME)' not in open(makefile_path).read():
            file.write("-> Error: rule `all' should call the rule `$(NAME)'\n")
        result = subprocess.run('make ' + '-C ' + project_path + ' all', shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
        file.write(result + '\n')
        if not os.path.exists(project_path + '/' + binary_name):
            file.write("-> Error when processing rule `fclean': It should have created {}\n".format(binary_name))
        if not glob.glob(project_path + '/*.o'):
            file.write("-> Error when processing rule `fclean': It should NOT have removed *.o\n")
        # todo:  [ -z "$(echo ${MAKEALLTWICE} | grep -i "Nothing to be done")" -a -z "$(echo ${MAKEALLTWICE} | grep -i "is up to date")" ] && printf "%s\n" "-> Failing rule: Processing the rule 'all' twice in a row should result in nothing to be done" && RET=1

        file.write("*------------------------------------------------------*\n")
        file.write("Checking rule: `clean'\n")
        if 'clean: ' not in open(makefile_path).read():
            file.write("-> Error: rule `clean' not found in the Makefile.\n")
        if not os.path.exists(project_path + '/' + binary_name):
            file.write("-> Error: Cannot test rule `clean' because rule `all' failed\n")
            # Stop the makefile test here
        result = subprocess.run('make ' + '-C ' + project_path + ' clean', shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
        file.write(result + '\n')
        if not os.path.exists(project_path + '/' + binary_name):
            file.write("-> Error: Failing Rule: It should not have cleaned the binary named {}.".format(binary_name))
        if glob.glob(project_path + '/*.o'):
            file.write("-> Error: Failing Rule: It should have cleaned the *.o")

        file.write("*------------------------------------------------------*\n")
        file.write("Checking rule: `re'\n")
        if 're: ' not in open(makefile_path).read():
            file.write("-> Error: rule `re' not found in the Makefile.\n")
        if not os.path.exists(project_path + '/' + binary_name):
            file.write("-> Error: Cannot test rule `re' because rule `all' failed\n")
        inode1 = os.stat(project_path + '/' + binary_name).st_ino
        file.write("-- Before running rule `re', the {} inode is {}\n".format(binary_name, inode1))
        result = subprocess.run('make ' + '-C ' + project_path + ' re', shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
        file.write(result + '\n')
        inode2 = os.stat(project_path + '/' + binary_name).st_ino
        file.write("-- After running rule `re', the {} inode is {}\n".format(binary_name, inode2))
        if not glob.glob(project_path + '/*.o'):
            file.write("-> Error when processing rule `re': It should have built the object file `*.o'\n")
        if not os.path.exists(project_path + '/' + binary_name):
            file.write("--> Error when processing rule `re': It should have compiled a binary named {}\n".format(binary_name))
        if inode1 == inode2:
            file.write("-> Failing rule `re': It should have compiled again the binary named {} (inode unchanged)\n".format(binary_name))

        file.write("*------------------------------------------------------*\n")
        file.write("Checking rule: `fclean'\n")
        if 'fclean: ' not in open(makefile_path).read():
            file.write("-> Error: rule `fclean' not found in the Makefile.\n")
        result = subprocess.run('make ' + '-C ' + project_path + ' fclean', shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
        file.write(result + '\n')
        if os.path.exists(project_path + '/' + binary_name):
            file.write("--> Error when processing rule `re': It should have removed the binary named {}\n".format(binary_name))
        if glob.glob(project_path + '/*.o'):
            file.write("-> Error: Failing Rule: It should have cleaned the *.o")
        if glob.glob(project_path + '/*.a'):
            file.write("-> Error: Failing Rule: It should have cleaned the *.a")

        file.write("*------------------------------------------------------*\n")
        file.write("Checking rule: `$(NAME)'\n")
        if '$(NAME):' not in open(makefile_path).read():
            file.write("-> Error: rule `$(NAME)' not found in the Makefile.\n")
        result = subprocess.run('make ' + '-C ' + project_path + ' ' + binary_name, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
        file.write(result + '\n')
        if not os.path.exists(project_path + '/' + binary_name):
            file.write("--> Error when processing rule `re': It should have compiled a binary named {}\n".format(binary_name))
        if not glob.glob(project_path + '/*.o'):
            file.write("-> Error when processing rule `fclean': It should NOT have removed *.o\n")
        # @todo :  [ -z "$(echo ${MAKEALLTWICE} | grep -i "Nothing to be done")" -a -z "$(echo ${MAKEALLTWICE} | grep -i "is up to date")" ] && printf "%s\n" "-> Failing rule: Processing the rule 'all' twice in a row should result in nothing to be done" && RET=1

        file.write("*------------------------------------------------------*\n")
        file.write("Checking rule: `.PHONY'\n")
        if '.PHONY:' not in open(makefile_path).read():
            file.write("-> Error: rule `.PHONY' not found in the Makefile.\n")
        if not os.path.exists(project_path + '/' + binary_name):
            file.write("-> Error: Cannot test rule `re' because rule `$(NAME)' failed\n")
        result = subprocess.run('make ' + '-C ' + project_path + ' .PHONY', shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
        file.write(result + '\n')
        if not os.path.exists(project_path + '/' + binary_name):
            file.write("--> Error when processing rule `.PHONY': It should not have cleaned the binary named {}\n".format(binary_name))
        if glob.glob(project_path + '/*.o'):
            file.write("-> Error: Failing Rule: It should have cleaned the *.o")
    return 0


def check_42_commandements(project_path:str):
    """
    :param project_path: The path of the project
    :return: Will return 0 if everything is ok,
     1 if the file doesn't exists,
     2 if the file content is different.
    """
    if not os.path.exists(project_path + '/rendu'):
        print("file `rendu' not found.")
        return 1
    with open(project_path + '/rendu', 'r') as file:
        content = file.read()
        if content != "En choisissant d'effectuer ma scolarite a 42, je declare adherer a ces regles ainsi qu'aux valeurs morales qu'elles vehiculent.\n":
            print("Error: The `rendu' file content is different from what is expected.")
            return 2
    return 0


def check_forbidden_functions(project_path: str, binary: str):
    # @todo: Refactor check_forbidden_functions to have a modular authorized_functions (to be used on multiple projects)
    authorized_functions = ['free', 'malloc', 'write', 'main']
    functions_called = []
    result = subprocess.run(['nm', project_path + '/' + binary], stdout=subprocess.PIPE).stdout.decode('utf-8')
    for line in result.splitlines():
        if "U _" in line:
            functions_called.append(re.sub(' +', ' ', line))
    sys_calls = {function.replace(' U _', '') for function in functions_called}
    sys_calls = [item for item in sys_calls if not item.startswith("ft_")]
    extra_function_call = [item for item in sys_calls if item not in authorized_functions]
    with open(os.path.dirname(os.path.realpath(__file__)) + "/.myforbiddenfunctions", 'w+') as file:
        for item in extra_function_call:
            file.write("You should justify the use of this function: `{}'\n".format(item))
    return 0


def check_libft(project_path: str):
    required_functions = ['libft.h', 'ft_strcat.c', 'ft_strncat.c',
                          'ft_strlcat.c', 'ft_strchr.c', 'ft_strnstr.c',
                          'ft_strrchr.c', 'ft_strclr.c', 'ft_strcmp.c',
                          'ft_strncmp.c', 'ft_strcpy.c', 'ft_strncpy.c',
                          'ft_strdel.c', 'ft_strdup.c', 'ft_strequ.c',
                          'ft_strnequ.c', 'ft_striter.c', 'ft_striteri.c',
                          'ft_strjoin.c', 'ft_strlen.c', 'ft_strmap.c',
                          'ft_strmapi.c', 'ft_strnew.c', 'ft_strstr.c',
                          'ft_strsplit.c', 'ft_strsub.c', 'ft_strtrim.c',
                          'ft_atoi.c', 'ft_itoa.c', 'ft_tolower.c',
                          'ft_toupper.c', 'ft_putchar.c', 'ft_putchar_fd.c',
                          'ft_putstr.c', 'ft_putstr_fd.c', 'ft_putnbr.c',
                          'ft_putnbr_fd.c', 'ft_putendl.c', 'ft_putendl_fd.c',
                          'ft_isalnum.c', 'ft_isalpha.c', 'ft_isascii.c',
                          'ft_isdigit.c', 'ft_isprint.c', 'ft_memalloc.c',
                          'ft_memchr.c', 'ft_memcmp.c', 'ft_memcpy.c',
                          'ft_memccpy.c', 'ft_memdel.c', 'ft_memmove.c',
                          'ft_memset.c', 'ft_bzero.c']
    bonus_functions = ['ft_lstnew.c', 'ft_lstdelone.c', 'ft_lstdel.c',
                       'ft_lstiter.c', 'ft_lstadd.c', 'ft_lstmap.c']
    while True:
        if all([os.path.isfile(project_path + '/' + function) for function in required_functions]):
            break
        else:
            print("ERROR: not all required files are here")
            break
    while True:
        if all([os.path.isfile(project_path + '/' + function) for function in bonus_functions]):
            break
        else:
            print("Warning: not all bonus files are here")
            break
    file_list = []
    for file in glob.glob(project_path + '/*.c'):
        file_list.append(file.replace(project_path + '/', ''))
    extra_functions = [item for item in file_list if item not in required_functions and item not in bonus_functions]
    print("You have {} extra functions.".format(len(extra_functions)))
    check_norme(project_path)
    with open(os.path.dirname(os.path.realpath(__file__)) + "/.mystatic", 'w+') as file:
        result = subprocess.run(['sh', 'check_static.sh', project_path], stdout=subprocess.PIPE).stdout.decode('utf-8')
        file.write(result)
    check_makefile(project_path, "libft.a") # @todo: Have number of errors printed for makefile check
    check_forbidden_functions(project_path, "libft.a")
    #moulitest
    #libft-unit-test
    #maintest
    return 0


sys.exit(check_forbidden_functions("/tmp/libft", "libft.a"))
