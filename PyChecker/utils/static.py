"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""
import subprocess


def check(root_path: str, args):
    print("*---------------------------------------------------------------*")
    print("*------------------------Static functions:----------------------*")
    print("*---------------------------------------------------------------*")
    with open(root_path + "/.mystatic", 'w+') as file:
        result = subprocess.run(['sh', root_path + '/scripts/check_static.sh', args.path],
                                stdout=subprocess.PIPE).stdout.decode('utf-8')
        file.write(result)
    # @todo: Replace check_static script with a python way of doing it
    print(result)
    return result
