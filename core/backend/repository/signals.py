from django.conf import settings
from django.db.models import signals

from repository.models import Repository, RepositoryAccess
from utils.system import remove_tree
from git.repo import Repo


def init_bare_repo_signal(sender, instance, created, **kwargs):
    """
        Initialize a bare git repository on server's deposit after it's creation.
    """

    if created:
        # Create repository folder under GIT_DEPOSIT_ROOT/username/repository.git and initialize it as bare.
        repository_location = Repo.get_repository_location(instance.owner.username, instance.name)
        repo = Repo(repository_location)
        repo.init_bare_repo()


def add_repo_access_signal(sender, instance, created, **kwargs):
    """
        Add creating user to the list of accessed users to this repository.
    """

    if created:
        repository_access = RepositoryAccess(user=instance.owner, repository=instance)
        repository_access.save()


def remove_repo_signal(sender, instance, using, **kwargs):
    """
        Remove repository folder from server deposit after it's deletion.
    """

    # Remove repository folder under GIT_DEPOSIT_ROOT/username/repository.git
    remove_tree(Repo.get_repository_location(instance.owner.username, instance.name))


signals.post_save.connect(init_bare_repo_signal, sender=Repository, weak=False)
signals.post_save.connect(add_repo_access_signal, sender=Repository, weak=False)
signals.post_delete.connect(remove_repo_signal, sender=Repository, weak=False)
