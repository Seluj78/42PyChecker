"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""
import os
from PyChecker.projects import libft

root_path = os.path.dirname(os.path.realpath(__file__))
libft.check("/tmp/libft", root_path)
