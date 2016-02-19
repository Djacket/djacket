import os
import shlex
import shutil
from subprocess import Popen, PIPE, STDOUT


def run_command(cmd, data, location, chw):
    """
        Runs command specified in 'cmd' and provides the input with the given data.
        Also if there is a location it will be appended to the end of command.
    """

    output = None
    cwd = os.getcwd()

    if location is not None and chw is True:
        cwd = location
    elif location is not None and chw is False:
        cmd = '{0} {1}'.format(cmd, location)

    r = Popen(shlex.split(cmd), stdout=PIPE, stdin=PIPE, stderr=PIPE, cwd=cwd)

    if data is None:
        output = r.communicate()[0].decode('utf-8')
    else:
        output = r.communicate(input=data)[0]

    return output


def remove_tree(path):
    """
        Removes a folder and it's whole tree from server storage.
    """

    shutil.rmtree(path, ignore_errors=True)


def rename_tree(path, new_name):
    """
        Renames a folder to it's new name.
    """

    parent = os.sep.join(path.split(os.sep)[:-1])
    os.rename(path, os.path.join(parent, new_name))
