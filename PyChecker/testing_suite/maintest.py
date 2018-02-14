"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import os
import re
import subprocess
import platform


def comment_define(source, destination, tokens):
    with open(source, 'r') as src, open(destination, 'w+') as dst:
        for line in src:
            for token in tokens:
                if re.match('#define\s+D_%s' % token.upper(), line):
                    line = '//{}//{}'.format(line, next(src))
                    break
            dst.write(line)


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
    # @todo special case for memalloc and memdel
    comment_define(root_path + '/testing_suites/Maintest/libft/main.c', root_path + '/libft_main.c', missing_functions)
    with open(root_path + "/.mymaintest", 'w+') as file:
        file.write("*------------------------------------------------------*\n")
        file.write("MAINTEST\n")
        file.write("Warning: This file contains escape sequences. Please use "
                   "`cat' to view it properly.\n")
        file.write("*------------------------------------------------------*\n")
        result = subprocess.run(['gcc', root_path + '/libft_main.c', '-L' + project_path,
                                 '-I' + project_path, "-I" + project_path +
                                 "/include", "-I" + project_path + "/includes",
                                 "-lft", "-o", root_path + "/libft_main.out"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT).stdout.decode('utf-8')
        file.write(result + '\n')
        print(result)
        result = subprocess.run([root_path + '/libft_main.out'], stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT).stdout.decode('utf-8')
        # @todo Count number of OK and FAILs and yellow tests to get score for maintest
        file.write(result + '\n')
        print(result)
    if platform.system() == "Linux":
        print("-- Disclaimer: Some of these test may fail where they woudn't on Darwin. (Because Linux ?)")
    os.remove(root_path + "/libft_main.c")
    os.remove(root_path + "/libft_main.out")
    # @todo Check if FAIL is the right keyword.
    return result.count("OK"), result.count("FAIL")
