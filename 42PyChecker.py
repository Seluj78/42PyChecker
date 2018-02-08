import os
import sys
import subprocess

def check_author_file(project_path: str):
    # @todo: Add a skip if author file set as optional
    author_fr = project_path + "/auteur"
    author_us = project_path + "/author"
    if os.path.exists(author_fr):
        output = subprocess.check_output("awk 'END {printf NR}' " + author_fr, shell=True)
    elif os.path.exists(author_us):
        output = subprocess.check_output("awk 'END {printf NR}' " + author_us, shell=True)
    else:
        print("Author file not found")
        sys.exit()  # @todo Add message if author file is set as optional
    if output != 1:
        print("Too many lines in author file (Or the file is empty)")
        sys.exit()  # @todo Add message if author file is set as optional or if project isn't solo

check_author_file("C:/Users/Jules/PycharmProjects/42PyChecker")
