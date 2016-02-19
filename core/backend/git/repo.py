import os

from django.conf import settings

from git.object import GIT_BLOB_OBJECT, GIT_TREE_OBJECT, GitTree, GitBlob, GitCommit
from utils.system import run_command
from utils.date import time_to_utc


class Repo:
    """
        Repository class for creating and working with a git repository. Repository object
            is created with an absolute path for a git repository. This absolute path can be
            specified in server deposit by using 'get_repository_location' static method in this class.
    """


    def __init__(self, location):
        self.location = location


    @staticmethod
    def get_repository_location(username, repository):
        """
            Returns absolute path of the given repository and username in server storage.
        """

        return os.path.join(settings.GIT_DEPOSIT_ROOT, username, '{0}.git'.format(repository))


    def is_valid(self):
        """
            Validity property to see if a git repository is available in the given location for object.
        """

        git_rev_parse = run_command(cmd='git rev-parse', data=None, location=self.location, chw=True)
        return len(git_rev_parse) == 0


    def init_bare_repo(self):
        """
            Initializes a bare git repository in the object location.
        """

        expected_location = os.path.join(settings.GIT_DEPOSIT_ROOT, self.location)
        if not os.path.exists(expected_location):
            os.makedirs(expected_location)
            run_command(cmd='git init --bare', data=None, location=expected_location, chw=False)


    def commit(self, payload):
        """
            Commits the given payload to this repository.
        """

        return run_command(cmd='git receive-pack --stateless-rpc', data=payload, location=self.location, chw=False)


    def pull(self, payload):
        """
            Pulls changes of this repository for pull or clone actions.
        """

        return run_command(cmd='git upload-pack --stateless-rpc', data=payload, location=self.location, chw=False)


    def get_last_update(self):
        """
            Returns latest update date of repository in "ISO 8601-like" format and 'UTC' timezone.
        """

        if not os.path.exists(self.location):
            return None

        git_output = run_command(cmd='git log -1 --format="%ai"', data=None, location=self.location, chw=True)
        if git_output is None or len(git_output) == 0:
            return None
        return time_to_utc(git_output.strip())


    def get_info_refs(self, service):
        """
            Returns 'refs' object information of the repository according to the given service.
        """

        return run_command(cmd='{0} --stateless-rpc --advertise-refs'.format(service),
                    data=None, location=self.location, chw=False)


    def get_latest_status(self):
        """
            Returns a status message of repository latest commit.

            e.g.
                'John Smith committed 9ece390, 2 hours ago'
        """

        return run_command(cmd='git log -1 --format="%cn committed %h, %cr"', data=None, location=self.location, chw=True)


    def get_commits(self, rev):
        """
            Returns all commits in all branches for this repository.
        """

        git_output = run_command(cmd='git log {0} --format="%H"'.format(rev),
                                    data=None, location=self.location, chw=True).split('\n')[:-1]

        return [GitCommit(repo=self, sha1_hash=commit, rev=rev) for commit in git_output]


    def get_contributers(self):
        """
            Returns all contributers in all branches for this repository.
        """

        return None


    def get_branches(self):
        """
            Returns all branches for this repository.
        """

        result = run_command(cmd='git branch', data=None, location=self.location, chw=True).split('\n')[:-1]
        branches = [item[2:] for item in result]
        return branches


    def get_head(self):
        """
            Returns HEAD revision for this repository.
        """

        return run_command(cmd='git rev-parse --abbrev-ref HEAD', data=None,
                    location=self.location, chw=True).split('\n')[:-1][0]


    def ls_tree(self, recursive, rev='HEAD'):
        """
            Lists contents of repository either in a recursive or non-recursive mode.
                Returns a list of GitTree/GitBlob objects representing contents.
        """

        r = '-r' if recursive else ''   # if recursive is set to 'True' then a '-r' option is added to command.
        cmd = 'git ls-tree --full-tree {0} {1}'.format(r, rev)
        git_output = run_command(cmd=cmd, data=None, location=self.location, chw=True).split('\n')[:-1]

        tree_contents = []
        for item in git_output:
            kind, path = item.split()[1], '{0}'.format(item.split()[3])
            if kind == GIT_BLOB_OBJECT:
                tree_contents.append(GitBlob(repo=self, path=path, rev=rev))
            elif kind == GIT_TREE_OBJECT:
                tree_contents.append(GitTree(repo=self, path=path, rev=rev))
        return tree_contents


    def __str__(self):
        """
            Returns a string representation of Repostiory's object.
        """

        return 'Git repository in {0}'.format(self.location)
