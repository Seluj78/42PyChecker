"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""
import os
import argparse
import platform
from PyChecker.projects import libft, ft_commandements, other, fillit
import sys


def check_args_rules(parser, args):
    """
    --verbose:                  Optionnal, no rules there.
    --no-gui:                   Enabled by default,
    --project:                  Required, Has a choice.
    --path:                     Required.

    --no-author:                Optionnal, no rules here expect 42commandements
    --no-forbidden-functions:   Optionnal, can only be set when project=fdf|fillit|ft_ls|ft_p|ft_printf|gnl\libft|libftasm|minishell|pushswap
    --no-makefile:              Optionnal, no rules here expect 42commandements
    --no-norm:                  Optionnal, no rules here expect 42commandements
    --no-static:                Optionnal, can only be set when project=libft
    --no-extra:                 Optionnal, can only be set when project=libft
    --no-required:              Optionnal, can only be set when project=libft
    --no-bonus:                 Optionnal, can only be set when project=libft
    --do-benchmark:             Optionnal, can only be set when project=libft
    --no-tests:                 Optionnal, can only be set when project is not other.
    --no-libftest:              Optionnal, can only be set when project=libft
    --no-maintest:              Optionnal, can only be set when project=libft|gnl|ft_ls
    --no-moulitest:             Optionnal, can only be set when project=libft|gnl|ft_ls|ft_printf|libftasm
    --no-fillit-checker:        Optionnal, can only be set when project=fillit
    --no-libft-unit-test:       Optionnal, can only be set when project=libft

    :param args: the parsed arguments passed to the program
    """

    # If no project is given the parser sends an error.
    if args.project is None:
        parser.error("You need to specify a project.")
    # If the path of the selected project is empty, the parser prints an error.
    if args.path == "":
        parser.error("`--path' needs to be specified in order for 42PyChecker"
                     " to know where your project is.")
    if args.path[0] != '/':
        parser.error("`--path' needs to have an absolute path")
    # If a test is disabled and the libft project is selected, the parser will
    # return an error.

    # Here, if the `--no-tests` option is set, all the testing suites will be
    # disabled, no matter the project.
    if args.project == "other" and args.no_tests:
        parser.error("`--no-tests' Can only be applied on projects, not when 'other' is selected.")

    if args.no_author and args.project == "42commandements":
        parser.error("`--no-author' Can only be applied on project, but not on 42commandements.")

    forbidden_functions_projects = ['fdf', 'fillit', 'ft_ls', 'ft_p', 'ft_printf', 'gnl', 'get_next_line', 'libft', 'libftasm', 'libft_asm', 'minishell', 'pushswap', 'push_swap']
    if args.no_forbidden_functions and args.project not in forbidden_functions_projects:
        parser.error("`--no-forbidden-functions' Cannot be set if project isn't one of " + str(forbidden_functions_projects))

    if args.no_makefile and args.project == "42commandements":
        parser.error("`--no-makefile' Can only be applied on project, but not on 42commandements.")

    if args.no_norm and args.project == "42commandements":
        parser.error("`--no-norm' Can only be applied on project, but not on 42commandements.")

    if args.no_static and args.project != "libft":
        parser.error("`--no-static' Can only be applied project `libft'")

    if args.no_extra and args.project != "libft":
        parser.error("`--no-extra' Can only be applied project `libft'")

    if args.no_required and args.project != "libft":
        parser.error("`--no-required' Can only be applied project `libft'")

    if args.no_bonus and args.project != "libft":
        parser.error("`--no-bonus' Can only be applied project `libft'")

    if args.do_benchmark and args.project != "libft":
        parser.error("`--do-benchmark' Can only be applied project `libft'")

    if args.no_libftest and args.project != "libft":
        parser.error("`--no-libftest' can only be applied if libft is selected "
                     "with `--project'")

    if args.no_maintest and args.project != "libft":
        parser.error("`--no-maintest' can only be applied if libft is selected "
                     "with `--project'")

    if args.no_moulitest and args.project != "libft":
        parser.error("`--no-moulitest' can only be applied if libft is selected"
                     " with `--project'")

    if args.no_libft_unit_test and args.project != "libft":
        parser.error("`--no-libft-unit-test' can only be applied if libft is selected"
                     " with `--project'")

    if args.no_fillit_checker and args.project != "fillit":
        parser.error("`--no-fillit-checker' can only be applied if fillit is selected"
                     " with `--project'")
    if args.no_tests:
        args.no_libftest = True
        args.no_maintest = True
        args.no_moulitest = True
        args.no_libft_unit_test = True
        args.no_fillit_checker = True


def print_header():
    """
    This function simply prints the warranty and condition statement.
    Might be removed in the future
    """
    print("\t42PyChecker  Copyright (C) 2018-present Jules Lasne "
          "<jules.lasne@gmail.com>\n\tThis program comes with"
          " ABSOLUTELY NO WARRANTY; for details run with `--show-w'.\n\tThis is free"
          " software, and you are welcome to redistribute it\n\tunder certain"
          " conditions; run with `--show-c' for details.")


def main():
    """
    Main function where arguments are parse and where the GUI is created.
    """

    # Initialize the parser and get the path of the script to use as a reference.
    root_path = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser()

    # @todo: Add verbose output
    # Adds all the arguments one by one.
    parser.add_argument("-v", "--verbose", help="Increases output verbosity",
                        action="store_true")
    parser.add_argument("--no-gui", help="disables the Graphical User Interface",
                        action="store_true")
    parser.add_argument("--project", help="Specifies the type of project you want to check", choices=['libft', '42commandements', 'other', 'fillit'], default=None)
    parser.add_argument("--no-libftest", help="Disables Libftest", action="store_true")
    parser.add_argument("--no-maintest", help="Disables Maintest", action="store_true")
    parser.add_argument("--no-moulitest", help="Disables Moulitest", action="store_true")
    parser.add_argument("--no-author", help="Disables author file check", action="store_true")
    parser.add_argument("--no-forbidden-functions", help="Disables forbidden functions check", action="store_true")
    parser.add_argument("--no-makefile", help="Disables Makefile check", action="store_true")
    parser.add_argument("--no-norm", help="Disables norm check", action="store_true")
    parser.add_argument("--no-static", help="Disables static functions check", action="store_true")
    parser.add_argument("--no-extra", help="Disables stats and checks on your extra functions", action="store_true")
    parser.add_argument("-p", "--path", help="The path of the project you want to test.", default="", type=str)
    parser.add_argument("--show-w", help="Displays the warranty warning from the license.", action="store_true")
    parser.add_argument("--show-c", help="Displays the conditions warning from the license.", action="store_true")
    parser.add_argument("--no-tests", help="Disables all the testing suites for the project.", action="store_true")
    parser.add_argument("--no-required", help="Disables required functions check", action="store_true")
    parser.add_argument("--no-libft-unit-test", help="Disables libft-unit-test", action="store_true")
    parser.add_argument("--do-benchmark", help="Enables libft-unit-test benchmarking", action="store_true")
    parser.add_argument("--no-fillit-checker", help="Disables fillit_checker", action="store_true")
    parser.add_argument("--no-bonus", help="Disables the bonus check for the libft", action="store_true")
    # Calls the parser for the arguments we asked to implement.
    args = parser.parse_args()

    # If the argument `--show-w` is passed, the program will display the warranty
    # statement and exit.
    if args.show_w:
        print("THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY"
              " APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING\n"
              " THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM"
              " “AS IS” WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR\n"
              " IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES"
              " OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE\n"
              " ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS"
              " WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME\n"
              " THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.")
        sys.exit()

    # If the `--show-c` argument is passed, the program will display the License
    # and exit.
    if args.show_c:
        with open(root_path + '/.github/LICENSE.lesser', 'r') as file:
            print(file.read())
        sys.exit()

    check_args_rules(parser, args)

    # Here we create the directory where the testing suites will be cloned
    if not os.path.exists(root_path + '/testing_suites'):
        os.makedirs(root_path + '/testing_suites')

    # Here we select the project and start the check based on the argument `--project`
    if args.project == "libft":
        libft.check(root_path, args)
    if args.project == "42commandements":
        ft_commandements.check(args)
    if args.project == "other":
        other.check(root_path, args)
    if args.project == "fillit":
        fillit.check(root_path, args)


if __name__ == '__main__':
    if not platform.system() == "Windows":
        try:
            print_header()
            main()
        except KeyboardInterrupt:
            sys.exit(1)
    else:
        raise OSError("Sorry, this script can't be run on windows !")
