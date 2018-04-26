import os, shlex, shutil, logging
from subprocess import PIPE, run

logger = logging.getLogger('django')


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

    result = run(shlex.split(cmd), input=data, stdout=PIPE, stderr=PIPE, cwd=cwd)

    if result.stderr != b'':
        logger.info('RUN_COMMAND -> ERR ({})'.format(result.stderr))

    if data is None:
        return result.stdout.decode('utf-8')
    else:
        return result.stdout


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
