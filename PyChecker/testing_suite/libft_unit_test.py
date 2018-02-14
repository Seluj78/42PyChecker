"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import platform
import subprocess

from chardet.universaldetector import UniversalDetector

detector = UniversalDetector()


def get_encoding_type(current_file):
    detector.reset()
    for line in open(current_file):
        detector.feed(line)
        if detector.done: break
    detector.close()
    return detector.result['encoding']


def convert(file: str, target:str):
    import codecs
    BLOCKSIZE = 1048576  # or some other, desired size in bytes
    with codecs.open(file, "r", get_encoding_type(file)) as sourceFile:
        with codecs.open(target, "w+", "utf-8") as targetFile:
            while True:
                contents = sourceFile.read(BLOCKSIZE)
                if not contents:
                    break
                targetFile.write(contents)


def run(root_path: str, args):
    print("*---------------------------------------------------------------*")
    print("*------------------------libft-unit-test------------------------*")
    print("*---------------------------------------------------------------*")
    if platform.system() != 'Darwin':
        print("Sorry, this testing suite can only be ran on Darwin computers (MacOS)")
        with open(root_path + '/.mylibftunittest', 'w+') as file:
            file.write("Sorry, this testing suite can only be ran on Darwin computers (MacOS)\n")
        return "Sorry, this testing suite can only be ran on Darwin computers (MacOS)"
    with open(root_path + '/.mylibftunittest', 'w+') as file:
        result = subprocess.run(['make', '-C', root_path + '/testing_suites/libft-unit-test', 'LIBFTDIR=' + args.path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8')
        file.write(result)
        print(result)
        result = subprocess.run(['make', 'f', '-C', root_path + '/testing_suites/libft-unit-test', 'LIBFTDIR=' + args.path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8')
        print(result)
        convert(root_path + '/testing_suites/libft-unit-test/result.log', root_path + '/result.log')
        with open(root_path + '/result.log', 'r') as file2:
            data = file2.read()
            file.write(data)
        if args.do_benchmark:
            result = subprocess.run([root_path + '/testing_suite/libft-unit-test/run_test', '-b'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8')
            print(result)
            file.write(result)
    # @todo return results from benchmark and tests