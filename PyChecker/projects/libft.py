"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import os
import glob
import subprocess
from PyChecker.Utils import author, forbidden_functions, makefile, norme
from PyChecker.Tests import maintest, moulitest, libftest


def check_bonuses(project_path: str, required_functions, bonus_functions):
    has_libft_bonuses = True
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
            has_libft_bonuses = False
            print("Warning: not all bonus files are here")
            break
    return has_libft_bonuses


def count_extras(project_path: str, required_functions, bonus_functions):
    file_list = []
    for file in glob.glob(project_path + '/*.c'):
        file_list.append(file.replace(project_path + '/', ''))
    extra_functions = [item for item in file_list if item not in required_functions and item not in bonus_functions]
    return extra_functions


def check(project_path: str, root_path: str):
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
    authorized_functions = ['free', 'malloc', 'write', 'main']
    extra_functions = count_extras(project_path, required_functions, bonus_functions)
    print("You have {} extra functions.".format(len(extra_functions)))
    author.check(project_path)
    norme.check(project_path, root_path)
    with open(root_path + "/.mystatic", 'w+') as file:
        result = subprocess.run(['sh', 'scripts/check_static.sh', project_path],
                                stdout=subprocess.PIPE).stdout.decode('utf-8')
        file.write(result)
    makefile.check(project_path, "libft.a", root_path)
    forbidden_functions.check(project_path, "libft.a", authorized_functions, root_path)
    libftest.run(project_path, root_path)
    has_libft_bonuses = check_bonuses(project_path, required_functions, bonus_functions)
    moulitest.run(project_path, has_libft_bonuses, "libft", root_path)
    maintest.run_libft(project_path, root_path)
    # @todo add libft-unit-test to the testing suite
    return 0
