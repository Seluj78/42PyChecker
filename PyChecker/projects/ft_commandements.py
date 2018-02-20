"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import os
import logging


def check(args):
    """
    This function will test the 42 commandements project.
    :param project_path: The path of the project to check

    :return: Will return 0 if everything is ok,
     1 if the file doesn't exists,
     2 if the file content is different.
    """
    logging.info("Started checks for project `42Commandements`")
    if not os.path.exists(args.path + '/rendu'):
        logging.critical("File rendu not found")
        print("file `rendu' not found.")
        return 1
    with open(args.path + '/rendu', 'r') as file:
        content = file.read()
        if content != "En choisissant d'effectuer ma scolarite a 42, je declare adherer a ces regles ainsi qu'aux valeurs morales qu'elles vehiculent.\n":
            logging.critical("Error: The `rendu' file content is different from what is expected.")
            print("Error: The `rendu' file content is different from what is expected.")
            return 2
    logging.info("Finished checks for project `42Commandements`")
    return 0
