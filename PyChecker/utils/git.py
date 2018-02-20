"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import subprocess
import shutil
import logging


def clone(repo: str, path: str):
    logging.info("Cloning repo {} in {}".format(repo, path))
    result = subprocess.run(['git', 'clone', repo, path, '--recursive'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).stdout.decode('utf-8')
    return result


def status(path: str):
    logging.info("Getting status from repo in {}".format(path))
    result = subprocess.run(['git', '--git-dir=' + path + '/.git', '--work-tree=' + path, 'status'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).stdout.decode('utf-8')
    # @todo: Parse git's output and return like 0/1
    return result


def reset(path: str):
    logging.info("Reseting repo located in {}".format(path))
    logging.debug("GIT: Executing `fetch origin`")
    result = subprocess.run(['git', '--git-dir=' + path + '/.git', '--work-tree=' + path, 'fetch', 'origin'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).stdout.decode('utf-8')
    logging.debug("GIT: Executing `reset --hard origin/master`")
    result += subprocess.run(['git', '--git-dir=' + path + '/.git', '--work-tree=' + path, 'reset', '--hard', 'origin/master'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).stdout.decode('utf-8')
    logging.debug("GIT: Executing `clean -f`")
    result += subprocess.run(['git', '--git-dir=' + path + '/.git', '--work-tree=' + path, 'clean', '-f'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).stdout.decode('utf-8')
    return result


def delete(path: str):
    logging.info("Deleting repo located at {}".format(path))
    shutil.rmtree(path)
    return


def remove(path: str):
    logging.info("Removing repo located at {}".format(path))
    delete(path)
