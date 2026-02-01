from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create test users for the application'

    def handle(self, *args, **options):
        users_data = [
            {'id': 1, 'username': 'alice', 'email': 'alice@example.com'},
            {'id': 2, 'username': 'bob', 'email': 'bob@example.com'},
            {'id': 3, 'username': 'charlie', 'email': 'charlie@example.com'},
        ]

        for user_data in users_data:
            user, created = User.objects.get_or_create(
                id=user_data['id'],
                defaults={
                    'username': user_data['username'],
                    'email': user_data['email'],
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created user: {user.username} (id={user.id})'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'User already exists: {user.username} (id={user.id})'
                    )
                )
