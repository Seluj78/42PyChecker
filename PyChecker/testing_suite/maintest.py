"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import os
import subprocess
import shutil


def run_libft(project_path: str, root_path: str):
    """
    This function will run the `maintest` to the given project.

    :param project_path: The path of the project you want to test.
    """
    print("*---------------------------------------------------------------*")
    print("*----------------------------Maintest---------------------------*")
    print("*---------------------------------------------------------------*")
    # These are the functions that the maintest tests for the libft.
    maintest_functions = ['memset', 'bzero', 'memcpy', 'memccpy', 'memmove',
                          'memchr', 'memcmp', 'strlen', 'strdup', 'strcpy',
                          'strncpy', 'strcat', 'strncat', 'strlcat', 'strchr',
                          'strrchr', 'strstr', 'strnstr', 'strcmp', 'strncmp',
                          'atoi', 'isalpha', 'isdigit', 'isalnum', 'isascii',
                          'isprint', 'toupper', 'tolower', 'strnew', 'strdel',
                          'strclr', 'striter', 'striteri', 'strmap', 'strmapi',
                          'strequ', 'strnequ', 'strsub', 'strjoin', 'strsplit',
                          'itoa', 'strtrim', 'lstnew', 'lstdelone', 'lstdel',
                          'lstadd', 'lstiter', 'lstmap']
    missing_functions = []
    for file in maintest_functions:
        # @todo Add a check to handle libft where file aren't at libft/ but can be in libft/src
        if not os.path.exists(project_path + '/ft_' + file + '.c'):
            missing_functions.append(file)
    # @todo: special case for memalloc and memdel
    missing = ""
    for function in missing_functions:
        missing = missing + '|D_' + function.upper()
    missing = missing[1:]
    # Has to be done, or else the last one is ignored. To be fixed !
    missing = missing + "|D_NOTHING"
    if missing == "":
        shutil.copy("testing_suites/Maintest/libft/main.c", "libft_main.c")
    else:
        # @todo: Silence error from script maintest.
        subprocess.run(['sh', 'scripts/remove_missing_functions_maintest.sh', missing])
    with open(root_path + "/.mymaintest", 'w+') as file:
        file.write("*------------------------------------------------------*\n")
        file.write("MAINTEST\n")
        file.write("Warning: This file contains escape sequences. Please use "
                   "`cat' to view it properly.\n")
        file.write("*------------------------------------------------------*\n")
        result = subprocess.run(['gcc', 'libft_main.c', '-L' + project_path,
                                 '-I' + project_path, "-I" + project_path +
                                 "/include", "-I" + project_path + "/includes",
                                 "-lft", "-o", "libft_main.out"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT).stdout.decode('utf-8')
        file.write(result + '\n')
        print(result)
        result = subprocess.run(['./libft_main.out'], stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT).stdout.decode('utf-8')
        # @todo: Count number of OK and FAILs and yellow tests to get score for maintest
        file.write(result + '\n')
        print(result)
    os.remove("libft_main.c")
    os.remove("libft_main.out")
