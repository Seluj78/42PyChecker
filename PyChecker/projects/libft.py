"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""
import os
import glob
from PyChecker.utils import author, forbidden_functions, makefile, norme, static
from PyChecker.testing_suite import maintest, moulitest, libftest
from PyChecker.testing_suite import libft_unit_test
import logging


def check_required(project_path: str, required_functions):
    logging.info("LIBFT: Started required function check.")
    while True:
        if all([os.path.isfile(project_path + '/' + function) for function in required_functions]):
            break
        else:
            logging.debug("LIBFT: ERROR: not all required files are here")
            print("--> ERROR: not all required files are here")
            logging.info("LIBFT: Finished required function check.")
            return "--> ERROR: not all required files are here"
    logging.debug("LIBFT: All required functions are present.")
    logging.info("LIBFT: Finished required function check.")
    return "-- All required functions are present."

def check_bonuses(project_path: str, bonus_functions):
    logging.info("LIBFT: Started bonus function check")
    has_libft_bonuses = True
    while True:
        if all([os.path.isfile(project_path + '/' + function) for function in bonus_functions]):
            logging.debug("LIBFT: Found all bonuses files")
            break
        else:
            has_libft_bonuses = False
            logging.warning("LIBFT: Warning: Warning: not all bonus files are here")
            print("--> Warning: not all bonus files are here")
            logging.info("LIBFT: Finished bonus function check")
            return has_libft_bonuses, "--> Warning: not all bonus files are here"
    logging.info("LIBFT: Finished bonus function check")
    return has_libft_bonuses, "-- All bonuses files were found."


def count_extras(project_path: str, required_functions, bonus_functions):
    logging.info("LIBFT: Started extra function count.")
    file_list = []
    for file in glob.glob(project_path + '/*.c'):
        file_list.append(file.replace(project_path + '/', ''))
    extra_functions = [item for item in file_list if item not in required_functions and item not in bonus_functions]
    print("*---------------------------------------------------------------*")
    print("*------------------------Extra functions:-----------------------*")
    print("*---------------------------------------------------------------*")
    print("You have {} extra functions.".format(len(extra_functions)))
    if extra_functions:
        logging.debug("Found extra functions:")
    for function in extra_functions:
        logging.debug(function)
        print(function)
    logging.info("LIBFT: Finished extra function count.")
    return extra_functions


def check(root_path: str, args):
    logging.info("Started check for project `libft`")
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
    if not args.no_author:
        author_results = author.check(args.path)
    if not args.no_required:
        required_results = check_required(args.path, required_functions)
    if not args.no_bonus:
        has_libft_bonuses, bonus_result = check_bonuses(args.path, bonus_functions)
    if not args.no_extra:
        extra_functions = count_extras(args.path, required_functions, bonus_functions)
    if not args.no_norm:
        norm_results = norme.check(args.path, root_path)
    if not args.no_static:
        static_results = static.check(root_path, args)
    if not args.no_makefile:
        makefile_results = makefile.check(args.path, root_path)
    if not args.no_forbidden_functions:
        forbidden_functions_results = forbidden_functions.check(args.path, authorized_functions, root_path)
    if not args.no_moulitest:
        moulitest_results = moulitest.run(args.path, has_libft_bonuses, "libft", root_path)
    if not args.no_libftest:
        libftest_results = libftest.run(args.path, root_path)
    if not args.no_maintest:
        maintest_ok, maintest_fail = maintest.run_libft(args.path, root_path)
    if not args.no_libft_unit_test:
        if args.do_benchmark:
            libft_unit_test_results, benchmark_results = libft_unit_test.run(root_path, args)
        else:
            libft_unit_test_results = libft_unit_test.run(root_path, args)

    print("\n\n\nThe results are in:\n")
    if not args.no_author:
        print("Author File: \n" + author_results + '\n')
    if not args.no_required:
        print("Required Functions: \n" + required_results + '\n')
    if not args.no_bonus:
        print("Bonus Functions: \n" + bonus_result + '\n')
    if not args.no_extra:
        # @todo: Stats on all c/h files of project, like with `cloc' ?
        print("Extra Functions: -- You have {}\n".format(len(extra_functions)))
    if not args.no_norm:
        print("Norme results: \n" + norm_results + '\n')
    if not args.no_static:
        print("Static Functions:\n" + static_results)
    if not args.no_makefile:
        print("Makefile: \n" + makefile_results + '\n')
    if not args.no_forbidden_functions:
        print("Forbidden Functions: \n" + forbidden_functions_results)
    if not args.no_moulitest:
        print("Moulitest: \n" + moulitest_results + '\n')
    if not args.no_libftest:
        print("Libftest: \nLibft Part One: " + libftest_results[0])
        print("Libft Part two: " + libftest_results[1])
        print("Libft Bonuses: " + libftest_results[2] + '\n')
    if not args.no_maintest:
        print("Maintest: \n{} OKs and {} FAILs.".format(maintest_ok, maintest_fail) + '\n')
    if not args.no_libft_unit_test:
        if args.do_benchmark:
            # @todo: Strip useless chars from benchmark results
            print('libft-unit-test: \n' + libft_unit_test_results + '\n\n' + benchmark_results + '\n')
        else:
            print('libft-unit-test: \n' + libft_unit_test_results + '\n')
    logging.info("Finished check for project `libft`")
    return 0
