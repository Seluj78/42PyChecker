"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""
from PyChecker.utils import author, norme, makefile
import logging


def check(root_path: str, args):
    logging.info("Starting check for project `other`")
    if not args.no_author:
        author.check(args.path)
    if not args.no_norm:
        norme.check(args.path, root_path)
    if not args.no_makefile:
        makefile.check(args.path, root_path)
    # @todo: Add forbidden function check based on assumption of what the project is.
    return 0
