from abc import ABCMeta, abstractmethod

from utils.system import run_command
from utils.date import time_to_utc

GIT_BLOB_OBJECT = 'blob'
GIT_TREE_OBJECT = 'tree'
GIT_COMMIT_OBJECT = 'commit'
GIT_VALID_OBJECT_KINDS = [GIT_BLOB_OBJECT, GIT_TREE_OBJECT, GIT_COMMIT_OBJECT]


class GitObject:
    """
        Represents a git object. Each GitObject is either a blob, tree or a commit which
            is represented in object's "kind" attribute.
        GitObject needs a Repository object as it's container and a revision.
            Then it will be located using it's repository, revision and path or sha1_hash
            depending on being a blob/tree or a commit object.


        * tag object will be implemented in future versions.
    """

    __metaclass__ = ABCMeta


    @abstractmethod
    def __init__(self, repo, kind, rev):
        assert repo is not None, 'Repository reference is not passed'
        assert repo.is_valid(), 'Entered repository is not valid'

        self.repo = repo
        self.kind = kind
        self.rev = rev


    def is_blob(self):
        """
            Returns true if this object is a blob.
        """

        return self.kind == GIT_BLOB_OBJECT


    def is_tree(self):
        """
            Returns true if this object is a tree.
        """

        return self.kind == GIT_TREE_OBJECT


    def is_commit(self):
        """
            Returns true if this object is a commit.
        """

        return self.kind == GIT_COMMIT_OBJECT


    def get_repo(self):
        """
            Returns repository of object.
        """

        return self.repo


    def get_kind(self):
        """
            Returns kind of object.
        """

        return self.kind


    def get_revision(self):
        """
            Returns revision of object.
        """

        return self.rev


    @abstractmethod
    def get_subject(self):
        pass


    @abstractmethod
    def get_committer_date(self):
        pass


    @abstractmethod
    def get_committer_email(self):
        pass


    @abstractmethod
    def get_committer_name(self):
        pass


    @abstractmethod
    def show(self):
        pass


class GitBlob(GitObject):
    """
        Represents a Git blob object.
        Path of object is needed for locating and getting blob's information.
    """

    def __init__(self, repo, path, rev='HEAD'):
        assert path is not None, 'Path of blob should not be None'

        super(GitBlob, self).__init__(repo, GIT_BLOB_OBJECT, rev)
        self.path = path


    def get_path(self):
        """
            Returns path of this blob in repository.
        """

        return self.path


    def get_subject(self):
        """
            Returns latest commit message given to this blob.
        """

        cmd = 'git log -1 --format="%s" {0} -- {1}'.format(self.rev, self.path)

        git_output = run_command(cmd=cmd, data=None, location=self.repo.location, chw=True).strip()
        return git_output


    def get_committer_date(self):
        """
            Returns latest commiter date for this blob in "ISO 8601-like" format and UTC timezone.
        """

        cmd = 'git log -1 --format="%ci" {0} -- {1}'.format(self.rev, self.path)

        git_output = run_command(cmd=cmd, data=None, location=self.repo.location, chw=True)
        return time_to_utc(git_output.strip())


    def get_committer_email(self):
        """
            Returns committer email.
        """

        cmd = 'git log -1 --format="%ce" {0} -- {1}'.format(self.rev, self.path)

        git_output = run_command(cmd=cmd, data=None, location=self.repo.location, chw=True).strip()
        return git_output


    def get_committer_name(self):
        """
            Returns committer name.
        """

        cmd = 'git log -1 --format="%cn" {0} -- {1}'.format(self.rev, self.path)

        git_output = run_command(cmd=cmd, data=None, location=self.repo.location, chw=True).strip()
        return git_output


    def show(self):
        """
            Reads content of blob and returns it as a pretty formated output.
        """

        level = '{0}:{1}'.format(self.rev, self.path)
        file_content = run_command(cmd='git cat-file -p {0}'.format(level), data=None, location=self.repo.location, chw=True)
        return file_content


    def __str__(self):
        """
            Returns a string representation of blob's object.
        """

        return 'GitBlob {0}, revision {1} for {2}'.format(self.path, self.rev, self.repo)


class GitTree(GitObject):
    """
        Represents a Git blob tree.
        Path of object is needed for locating and getting tree's information.
    """

    def __init__(self, repo, path, rev='HEAD'):
        assert path is not None, 'Path of tree should not be None'

        super(GitTree, self).__init__(repo, GIT_TREE_OBJECT, rev)
        self.path = path


    def get_path(self):
        """
            Returns path of this tree in repository.
        """

        return self.path


    def get_subject(self):
        """
            Returns latest commit message given to this tree.
        """

        cmd = 'git log -1 --format="%s" {0} -- {1}'.format(self.rev, self.path)

        git_output = run_command(cmd=cmd, data=None, location=self.repo.location, chw=True).strip()
        return git_output


    def get_committer_date(self):
        """
            Returns latest commiter date for this tree in "ISO 8601-like" format and UTC timezone.
        """

        cmd = 'git log -1 --format="%ci" {0} -- {1}'.format(self.rev, self.path)

        git_output = run_command(cmd=cmd, data=None, location=self.repo.location, chw=True)
        return time_to_utc(git_output.strip())


    def get_committer_email(self):
        """
            Returns committer email.
        """

        cmd = 'git log -1 --format="%ce" {0} -- {1}'.format(self.rev, self.path)

        git_output = run_command(cmd=cmd, data=None, location=self.repo.location, chw=True).strip()
        return git_output


    def get_committer_name(self):
        """
            Returns committer name.
        """

        cmd = 'git log -1 --format="%cn" {0} -- {1}'.format(self.rev, self.path)

        git_output = run_command(cmd=cmd, data=None, location=self.repo.location, chw=True).strip()
        return git_output


    def show(self):
        """
            Returns content of tree object which may be other trees or blobs.
        """

        level = '{0}:{1}'.format(self.rev, self.path)
        cmd = 'git ls-tree --full-tree {0}'.format(level)
        git_output = run_command(cmd=cmd, data=None, location=self.repo.location, chw=True).split('\n')[:-1]

        tree_contents = []
        for item in git_output:
            kind, path = item.split()[1], '{0}/{1}'.format(self.path, item.split()[3])
            if kind == GIT_BLOB_OBJECT:
                tree_contents.append(GitBlob(repo=self.repo, path=path, rev=self.rev))
            elif kind == GIT_TREE_OBJECT:
                tree_contents.append(GitTree(repo=self.repo, path=path, rev=self.rev))
        return tree_contents


    def __str__(self):
        """
            Returns a string representation of tree's object.
        """

        return 'GitTree {0}, revision {1} for {2}'.format(self.path, self.rev, self.repo)


class GitCommit(GitObject):
    """
        Represents a Git commit object.
        SHA1 hash of object is needed for locating and getting object's information.
    """

    def __init__(self, repo, sha1_hash, rev='HEAD'):
        assert sha1_hash is not None, 'SHA-1 hash of commit should not be None'

        super(GitCommit, self).__init__(repo, GIT_COMMIT_OBJECT, rev)
        self.sha1_hash = sha1_hash


    def get_sha1_hash(self):
        """
            Returns SHA-1 hash of commit.
        """

        return self.sha1_hash


    def get_subject(self):
        """
            Returns latest commit message given to this commit.
        """

        cmd='git log -1 --format="%s" {0}'.format(self.sha1_hash)

        git_output = run_command(cmd=cmd, data=None, location=self.repo.location, chw=True).strip()
        return git_output


    def get_committer_date(self):
        """
            Returns latest commiter date for this commit in "ISO 8601-like" format and UTC timezone.
        """

        cmd='git log -1 --format="%ci" {0}'.format(self.sha1_hash)

        git_output = run_command(cmd=cmd, data=None, location=self.repo.location, chw=True)
        return time_to_utc(git_output.strip())


    def get_committer_email(self):
        """
            Returns committer email.
        """

        cmd='git log {0} -1 --format="%ce" {1}'.format(self.rev, self.sha1_hash)

        git_output = run_command(cmd=cmd, data=None, location=self.repo.location, chw=True).strip()
        return git_output


    def get_committer_name(self):
        """
            Returns committer name.
        """

        cmd='git log {0} -1 --format="%cn" {1}'.format(self.rev, self.sha1_hash)

        git_output = run_command(cmd=cmd, data=None, location=self.repo.location, chw=True).strip()
        return git_output


    def show(self):
        """
            Returns information about commit.
        """

        cmd = 'git show {0}'.format(self.sha1_hash)

        git_output = run_command(cmd=cmd, data=None, location=self.repo.location, chw=True)
        return git_output


    def __str__(self):
        """
            Returns a string representation of commit's object.
        """

        return 'Commit {0}, revision {1} for {1}'.format(self.sha1_hash, self.rev, self.repo)
