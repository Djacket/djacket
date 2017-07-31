from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
        Creates a default admin user if there is not any.
    """

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)


    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('admin', 'admin@djacket.io', 'lukedidntknow')
