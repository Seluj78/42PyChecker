"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""
import subprocess, logging


def check(root_path: str, args):
    """

    :param root_path: The absolute path leading to the script's main file.
    :param args: The CLI arguments passed to the program

    :return: Returns whatever returned the static function check.
    """
    logging.info("Starting static functions check")
    print("*---------------------------------------------------------------*")
    print("*------------------------Static functions:----------------------*")
    print("*---------------------------------------------------------------*")
    # Open the file .mystatic to write the results in it
    with open(root_path + "/.mystatic", 'w+') as file:
        logging.debug("Opened file {}.".format(root_path + "/.mystatic"))
        # @todo: Replace check_static script with a python way of doing it
        # Run the check_static.sh script and get the output
        logging.info("STATIC: Running script {}.".format(root_path + '/scripts/check_static.sh'))
        result = subprocess.run(['sh', root_path + '/scripts/check_static.sh',
                                 args.path], stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT).stdout.decode('utf-8')
        file.write(result)
    print(result)
    logging.info("Finished static functions check")
    return result
