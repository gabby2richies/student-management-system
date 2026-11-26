import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        username = os.environ.get('ADMIN_USERNAME')
        email = os.environ.get('ADMIN_EMAIL')
        password = os.environ.get('ADMIN_PASSWORD')

        if not username or not email or not password:
            self.stdout.write('Admin environment variables are missing.')
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email}
        )

        if created:
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write('Administrator account created.')
        else:
            self.stdout.write('Administrator account already exists.')