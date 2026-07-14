import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create or reset the production admin account"

    def handle(self, *args, **options):
        email = os.environ.get("DJANGO_ADMIN_EMAIL")
        password = os.environ.get("DJANGO_ADMIN_PASSWORD")

        if not email or not password:
            raise CommandError(
                "DJANGO_ADMIN_EMAIL and DJANGO_ADMIN_PASSWORD "
                "must be configured."
            )

        User = get_user_model()

        user, created = User.objects.get_or_create(email=email)

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS("Production admin created successfully.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("Production admin reset successfully.")
            )