import os
import sys
import glob
import subprocess


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


def check_42_commandements(project_path:str):
    """
    :param project_path: The path of the project where you want to check the author file
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


sys.exit(check_42_commandements("/tmp/jlasne3"))
