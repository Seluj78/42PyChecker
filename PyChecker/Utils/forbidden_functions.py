"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import os
import subprocess
import re


def check(project_path: str, binary: str, authorized_func, root_path: str):
    """
    This function will check the functions used by the given binary in the given project.

    :param project_path: The path of the project you want to test.
    :param binary_name: The binary that you want to analyze
    :param authorized_func: The functions authorized by the project.
    """
    functions_called = []
    # @todo Check difference between Darwin and Linux `nm'
    result = subprocess.run(['nm', project_path + '/' + binary],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).stdout.decode('utf-8')
    for line in result.splitlines():
        if "U " in line:
            functions_called.append(re.sub(' +', ' ', line))
    sys_calls = {func.replace(' U ', '') for func in functions_called}
    sys_calls = [item for item in sys_calls if not item.startswith("ft_")]
    extra_function_call = [item for item in sys_calls if item not in authorized_func]
    with open(root_path + "/.myforbiddenfunctions", 'w+') as file:
        for item in extra_function_call:
            # This is to ignore functions like `__stack_chk_fail'
            if not item.startswith("__"):
                file.write("You should justify the use of this function: `{}'\n".format(item))
    return 0
