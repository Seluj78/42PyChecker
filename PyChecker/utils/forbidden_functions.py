"""
    Copyright (C) 2018 Jules Lasne <jules.lasne@gmail.com>
    See full notice in `LICENSE'
"""

import platform
import subprocess
import re
import logging


def check(project_path: str, authorized_func, root_path: str):
    """
    This function will check the functions used by the given binary in the given project.

    :param project_path: The path of the project you want to test.
    :param binary_name: The binary that you want to analyze
    :param authorized_func: The functions authorized by the project.
    """
    logging.info("Starting forbidden function check.")
    print("*---------------------------------------------------------------*")
    print("*----------------------Forbidden functions:---------------------*")
    print("*---------------------------------------------------------------*")
    ret = ""
    functions_called = []

    # Get binary name
    try:
        with open(project_path + '/Makefile', 'r') as file:
            data = file.read()
            binary = re.findall("NAME[\s]*=[\s]*(.*)", data)[0]
    except FileNotFoundError:
        logging.error("Makefile not found at {}".format(project_path))
        print(project_path + '/Makefile: File not found. Stopping')
        return project_path + '/Makefile: File not found. Stopping'

    logging.debug("FORBIDDEN: Running `make -C {} all".format(project_path))
    subprocess.run(['make', '-C', project_path, 'all'])
    logging.debug("FORBIDDEN: Running `nm {}`".format(project_path + '/' + binary))
    result = subprocess.run(['nm', project_path + '/' + binary],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).stdout.decode('utf-8')
    # @todo: Add detailed log for forbidden functions
    for line in result.splitlines():
        if "U " in line:
            functions_called.append(re.sub(' +', ' ', line))

    # Os check for nm differences
    logging.debug("FORBIDDEN: Checking OS")
    if platform.system() == "Darwin":
        sys_calls = {func.replace(' U _', '') for func in functions_called}
    elif platform.system() == "Linux":
        sys_calls = {func.replace(' U ', '') for func in functions_called}
    else:
        sys_calls = ['Error']

    sys_calls = [item for item in sys_calls if not item.startswith("ft_")]
    if platform.system() == "Linux":
        for i, calls in enumerate(sys_calls):
            sys_calls[i] = calls.split('@', 1)[0]
    extra_function_call = [item for item in sys_calls if item not in authorized_func]
    logging.debug("FORBIDDEN: Opening file {}.".format(root_path + "/.myforbiddenfunctions"))
    with open(root_path + "/.myforbiddenfunctions", 'w+') as file:
        for item in extra_function_call:
            # This is to ignore functions like `__stack_chk_fail'
            if not item.startswith("__"):
                logging.warning("You should justify the use of this function: `{}'".format(item))
                file.write("You should justify the use of this function: `{}'\n".format(item))
                print("You should justify the use of this function: `{}'".format(item))
                ret += "You should justify the use of this function: `{}'\n".format(item)
    logging.info("Finished forbidden function check.")
    return ret
