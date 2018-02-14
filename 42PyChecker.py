"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""
import os
import argparse
import platform
from PyChecker.projects import libft, ft_commandements, other
# @todo Add verbose output


def print_header():
    print("\t42PyChecker  Copyright (C) 2018-present Jules Lasne "
          "<jules.lasne@gmail.com>\n\tThis program comes with"
          " ABSOLUTELY NO WARRANTY; for details run with `--show-w'.\n\tThis is free"
          " software, and you are welcome to redistribute it\n\tunder certain"
          " conditions; run with `--show-c' for details.")


def main():
    root_path = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Increases output verbosity",
                        action="store_true")
    parser.add_argument("--no-gui", help="disables the Graphical User Interface",
                        action="store_true")
    parser.add_argument("--project", help="Specifies the type of project you want to check", choices=['libft', '42commandements', 'other'], default=None)
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
    # @todo Check what option is given based on the selected project.
    parser.add_argument("--no-required", help="Disables required functions check", action="store_true")
    parser.add_argument("--no-libft-unit-test", help="Disables libft-unit-test", action="store_true")
    parser.add_argument("--no-benchmark", help="Disables libft-unit-test benchmarking", action="store_false")

    args = parser.parse_args()
    if args.show_w:
        print_header()
        print("THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY"
              " APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING\n"
              " THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM"
              " “AS IS” WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR\n"
              " IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES"
              " OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE\n"
              " ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS"
              " WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME\n"
              " THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.")
        return
    if args.show_c:
        print_header()
        with open(root_path + '/.github/LICENSE.lesser', 'r') as file:
            print(file.read())
        return
    if args.no_tests:
        args.no_libftest = True
        args.no_maintest = True
        args.no_moulitest = True
    if args.project is None:
        parser.error("You need to specify a project.")
    if args.path == "":
        parser.error("`--path' needs to be specified in order for 42PyChecker"
                     " to know where your project is.")
    if args.no_libftest and args.project != "libft":
        parser.error("`--no-libftest' can only be applied if libft is selected "
                     "with `--project'")
    if args.no_maintest and args.project != "libft":
        parser.error("`--no-maintest' can only be applied if libft is selected "
                     "with `--project'")
    if args.no_moulitest and args.project != "libft":
        parser.error("`--no-moulitest' can only be applied if libft is selected"
                     " with `--project'")
    print_header()
    if args.project == "libft":
        libft.check(root_path, args)
    # @todo Handle options for 42commandements: No option can be passed (like --no-norm)
    if args.project == "42commandements":
        ft_commandements.check(args)
    # @todo Handle options for other: No option can be passed (like --no-norm)
    if args.project == "other":
        other.check(root_path, args)


if __name__ == '__main__':
    if not platform.system() == "Windows":
        main()
    else:
        raise OSError("Sorry, this script can't be run on windows !")
