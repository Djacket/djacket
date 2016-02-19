from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from djacket.storage import OverwriteStorage
from repository.models import Repository

FULLNAME_MAX_LENGTH = 32


def user_avatar_path(instance, filename):
    """
        Returns the path for user's avatar image under MEDIA_ROOT folder.

        e.g.
            MEDIA_ROOT/avatars/username/avatar.png
    """

    # Select username, 'avatar' static name and then file extention.
    return 'avatars/{0}/{1}.{2}'.format(instance.user.username, 'avatar', filename.split('.')[-1])


class UserProfile(models.Model):
    """
        A one-to-one model for keeping each user's extra information.
            This model is created with signal when a user signs up.
    """

    user = models.OneToOneField(User)
    name = models.CharField(max_length=FULLNAME_MAX_LENGTH)
    avatar = models.ImageField(upload_to=user_avatar_path, storage=OverwriteStorage())
    birthdate = models.DateTimeField(null=True)


    def __str__(self):
        return '{0}\'s Profile [id={1}]'.format(self.user.username, self.user.id)


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])   # Assign .profile property for each user object.


# Send signals for operations needed after user object is saved.
from user.signals import *
