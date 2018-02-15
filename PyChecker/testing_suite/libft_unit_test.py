"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import platform
import subprocess
import os
import io


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
        file.write(result)
        os.rename(root_path + '/testing_suites/libft-unit-test/result.log', root_path + '/.mylibftunittest-results')
        if args.do_benchmark:
            result = subprocess.run([root_path + '/testing_suites/libft-unit-test/run_test', '-b'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8')
            print(result)
            file.write(result)
    # @todo: return results from benchmark
    with io.open(root_path + '/.mylibftunittest-results', "r", encoding="ISO-8859-1") as file:
        data = file.read()
        results = 'OKs: ' + str(data.count('OK')) + '\n'
        results += 'KOs: ' + str(data.count('KO')) + '\n'
        results += 'FAILED: ' + str(data.count('FAILED')) + '\n'
        results += 'NO CRASH: ' + str(data.count('NO CRASH')) + '\n'
        results += 'protected: ' + str(data.count('protected')) + '\n'
        results += 'not protected:' + str(data.count('not protected'))
    print(results)
    return results