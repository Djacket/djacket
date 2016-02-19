GIT_SERVICE_UPLOAD_PACK = 'git-upload-pack'
GIT_SERVICE_RECEIVE_PACK = 'git-receive-pack'
GIT_SERVICES = [GIT_SERVICE_UPLOAD_PACK, GIT_SERVICE_RECEIVE_PACK]


def is_valid_git_service(service):
    """
        Returns true if the given service is one of git valid service packs.
    """

    return service in GIT_SERVICES
