import os
import random

from django.contrib.auth.models import User
from django.db.models import signals
from django.conf import settings

from user.models import UserProfile
from utils.system import remove_tree


def create_user_profile_signal(sender, instance, created, **kwargs):
    """
        Create UserProfile object when user signs up for the first time.
    """

    if created:
        stock_avatar_id = random.randint(0, 9) + 1
        UserProfile.objects.create(user=instance, avatar='./stock/{0}.png'.format(stock_avatar_id))


def create_user_fullname(sender, instance, created, **kwargs):
    """
        Create user's full name based on his/her first name and last name.
    """

    profile = UserProfile.objects.get(user_id=instance.id)
    profile.name = '{0} {1}'.format(instance.first_name, instance.last_name)
    profile.save()


def create_user_deposit_signal(sender, instance, created, **kwargs):
    """
        Create user's deposit folder when he/she registers on site.
    """

    if created:
        # Create user's deposit folder under GIT_DEPOSIT_ROOT/username
        os.makedirs(os.path.join(settings.GIT_DEPOSIT_ROOT, instance.username))


def delete_user_deposit_signal(sender, instance, using, **kwargs):
    """
        Delete user's deposit folder when it's account is deleted.
    """

    # Remove user's deposit folder under GIT_DEPOSIT_ROOT/username
    remove_tree(os.path.join(settings.GIT_DEPOSIT_ROOT, instance.username))


signals.post_save.connect(create_user_profile_signal, sender=User, weak=False)
signals.post_delete.connect(delete_user_deposit_signal, sender=User, weak=False)
signals.post_save.connect(create_user_deposit_signal, sender=User, weak=False)
signals.post_save.connect(create_user_fullname, sender=User, weak=False)
