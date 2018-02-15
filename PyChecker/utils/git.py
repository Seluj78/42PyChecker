"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import subprocess
import shutil


def clone(repo: str, path: str):
    result = subprocess.run(['git', 'clone', repo, path, '--recursive'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).stdout.decode('utf-8')
    return result


def status(path: str):
    result = subprocess.run(['git', '--git-dir=' + path + '/.git', '--work-tree=' + path, 'status'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).stdout.decode('utf-8')
    # @todo: Parse git's output and return like 0/1
    return result


def reset(path: str):
    result = subprocess.run(['git', '--git-dir=' + path + '/.git', '--work-tree=' + path, 'fetch', 'origin'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).stdout.decode('utf-8')
    result += subprocess.run(['git', '--git-dir=' + path + '/.git', '--work-tree=' + path, 'reset', '--hard', 'origin/master'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).stdout.decode('utf-8')
    result += subprocess.run(['git', '--git-dir=' + path + '/.git', '--work-tree=' + path, 'clean', '-f'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).stdout.decode('utf-8')
    return result


def delete(path: str):
    shutil.rmtree(path)
    return


def remove(path: str):
    delete(path)
