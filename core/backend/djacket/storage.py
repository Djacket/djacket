import os

from django.core.files.storage import FileSystemStorage
from django.conf import settings


class OverwriteStorage(FileSystemStorage):
    """
        Overwrites to a file if it exists on file system.
    """

    def get_available_name(self, name, max_length=None):
        """
            If a file with the given name exists in MEDIA_ROOT,
                it will be removed otherwise it's name is returned.
        """

        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name
