from __future__ import division
import models as m
import subprocess
import time
import datetime as dt
import ast
import pdb


def run_ssh_command(cmd, timeout=10, server="Jonathan@128.3.12.69", arg=[]):
    """
    Send a ssh request and check if the request is not hanging.
    timeout [seconds]
    """
    # Launch ssh query
    long_cmd = ["ssh", server, "python", cmd]
    long_cmd.extend(arg)
    ssh = subprocess.Popen(long_cmd, shell=False, stdout=subprocess.PIPE,
                           bufsize=1000000, stderr=subprocess.PIPE)

    if not timeout:
        return ssh.stdout.readlines(), 'Success'

    else:
        # Test for output every second
        for step in range(0, timeout):
            time.sleep(1)
            if ssh.poll() is not None:
                return ssh.stdout.readlines(), 'Success'

    # The ssh query was longer than timeout duration
    ssh.kill()
    return False, ssh.stderr.readlines()


def parse_ssh_dict(output, keys, status):
    """
    Parse the output of an ssh request.
    Output lenght must be the same as keys lenght.
    """
    # Check if the lenght is the same
    if len(output) != len(keys):
        print('#####')
        print('output:' + str(output))
        print('status:' + str(status))
        print('#####')
        raise Exception('The output from the ssh request was not the right lenght')

    # Parse the string
    result = {}
    for key, string in zip(keys, output):
        dict_string = '{' + string.split('{', 1)[1].split('}')[0] + '}'
        result[key] = ast.literal_eval(dict_string)

    return result


def parse_ssh_list(output, status):
    """
    Parse the output from a dataframe where every row is a different line
    """
    result = []
    for string in output:
        dict_string = '{' + string.split('{', 1)[1].split('}')[0] + '}'
        result.append(ast.literal_eval(dict_string))

    return result
