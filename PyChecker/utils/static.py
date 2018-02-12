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
        result = subprocess.run(['sh', 'scripts/check_static.sh', args.path],
                                stdout=subprocess.PIPE).stdout.decode('utf-8')
        file.write(result)
    # @todo Fix error message from script.
    print(result)
    return result
