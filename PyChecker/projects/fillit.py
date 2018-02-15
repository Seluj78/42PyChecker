"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

from PyChecker.utils import author, norme, makefile, forbidden_functions
from PyChecker.testing_suite import fillit_checker


def check(root_path: str, args):

    authorized_functions = ['exit', 'open', 'close', 'write', 'read', 'malloc',
                            'free', 'main']

    # @todo: check for flags in makefile (no opti flags allowed).
    if not args.no_author:
        author_results = author.check(args.path)
    if not args.no_norm:
        norm_results = norme.check(args.path, root_path)
    if not args.no_makefile:
        makefile_results = makefile.check(args.path, root_path)
    if not args.no_forbidden_functions:
        forbidden_functions_results = forbidden_functions.check(args.path, authorized_functions, root_path)
    if not args.no_fillit_checker:
        fillit_checker_results = fillit_checker.run(root_path, args.path)

    print("\n\n\nThe results are in:\n")
    if not args.no_author:
        print("Author File: \n" + author_results + '\n')
    if not args.no_norm:
        print("Norme results: \n" + norm_results + '\n')
    if not args.no_makefile:
        print("Makefile: \n" + makefile_results + '\n')
    if not args.no_forbidden_functions:
        print("Forbidden Functions: \n" + forbidden_functions_results)
    if not args.no_fillit_checker:
        print("Fillit Checker: \n" + fillit_checker_results)
    return 0
