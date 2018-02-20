"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import os
import glob
import subprocess
import logging


def check(project_path: str, root_path: str):
    """
    This function will check the norm of the given project.

    :param project_path: The path of the project where you want to check the author file
    :param root_path: The absolute path leading to the script's main file.

    :return: Returns a string containing either the number or errors or an error message
    """
    logging.info("Starting norme check.")
    print("*---------------------------------------------------------------*")
    print("*----------------------------NORM-------------------------------*")
    print("*---------------------------------------------------------------*")
    files = ""
    # Count and store all the .c and .h files in a variable
    logging.info("NORME: Discovering files for selected project")
    for filename in glob.iglob(project_path + '/**/*.c', recursive=True):
        logging.debug("Found file {}".format(filename))
        files += ' ' + filename
    for filename in glob.iglob(project_path + '/**/*.h', recursive=True):
        logging.debug("Found file {}".format(filename))
        files += ' ' + filename
    if files == "":
        logging.error("NORME: Didn't find any .c/h file to check")
        print("-- No source file (.c) or header (.h) to check")
        return "-- No source file (.c) or header (.h) to check"

    with open(root_path + "/.mynorme", 'w+') as file:
        logging.debug("Opening file {}.".format(root_path + "/.mynorme"))
        try:
            # Run the norminette on those files
            logging.info("Running command `norminette`")
            result = subprocess.run(['norminette'] + files.split(),
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT).stdout.decode('utf-8')
        except FileNotFoundError:
            logging.error("NORME: Error: Norminette not found")
            file.write("Error: Norminette not found.\n")
            print("--> Error: `norminette': command not found.")
            return "--> Error: `norminette': command not found."
        else:
            file.write(result)
            logging.debug("NORME: Counting norminette errors")
            error_count = result.count('Error')
            warning_count = result.count('Warning')
            if error_count != 0 or warning_count != 0:
                logging.debug("NORME: Found {} errors and {} warnings".format(error_count,
                                                               warning_count))
                logging.info("Finished norme checking")
                print("--> Found {} errors and {} warnings".format(error_count,
                                                               warning_count))
                return "--> Found {} errors and {} warnings".format(error_count,
                                                               warning_count)
    logging.debug("NORME: Found no norme errors.")
    logging.info("Finished norme checking")
    print("-- NTR (Nothing to Report)")
    return "-- NTR (Nothing to Report)"
