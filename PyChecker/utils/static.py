"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""
import subprocess


def check(root_path: str, args):
    """

    :param root_path: The absolute path leading to the script's main file.
    :param args: The CLI arguments passed to the program

    :return: Returns whatever returned the static function check.
    """
    print("*---------------------------------------------------------------*")
    print("*------------------------Static functions:----------------------*")
    print("*---------------------------------------------------------------*")
    # Open the file .mystatic to write the results in it
    with open(root_path + "/.mystatic", 'w+') as file:
        # @todo: Replace check_static script with a python way of doing it
        # Run the check_static.sh script and get the output
        result = subprocess.run(['sh', root_path + '/scripts/check_static.sh',
                                 args.path], stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT).stdout.decode('utf-8')
        file.write(result)
    print(result)
    return result
