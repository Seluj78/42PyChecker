"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import os


def check(project_path: str):
    """
    This function will check the author file for the given project.

    :param project_path: The path of the project where you want to check the author file

    :return: This function will return 0 if everything is ok,
     1 if file not found,
     2 if there's too many lines in the file,
     3 if the newline char is missing in the end of line
    """
    # @todo message and handle multiple authors
    print("*---------------------------------------------------------------*")
    print("*--------------------------Author file--------------------------*")
    print("*---------------------------------------------------------------*")
    author_fr = project_path + "/auteur"
    author_us = project_path + "/author"
    if os.path.exists(author_fr):
        count = len(open(author_fr).readlines())
        author = "fr"
    elif os.path.exists(author_us):
        count = len(open(author_us).readlines())
        author = "us"
    else:
        print("--> Error: Author file not found")
        return "--> Error: Author file not found"
    if count != 1:
        print("--> Error: Too many lines in author file (Or the file is empty)")
        return "--> Error: Too many lines in author file (Or the file is empty)"
    if author == "fr":
        with open(author_fr, 'r') as file:
            content = file.read()
            if "\n" not in content:
                print("--> Error: Missing <newline> character at the end of line")
                return "--> Error: Missing <newline> character at the end of line"
    elif author == "us":
        with open(author_us, 'r') as file:
            content = file.read()
            if "\n" not in content:
                print("--> Error: Missing <newline> character at the end of line")
                return "--> Error: Missing <newline> character at the end of line"
    print("-- NTR (Nothing to Report)")
    return "-- NTR (Nothing to Report)"
