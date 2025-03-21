from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
# from core.models import YourModel  # TODO: Import other models here
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Setup and seed the database with users and other data'

    def handle(self, *args, **kwargs):
        # 1. Clear existing data (Optional)
        self.stdout.write(self.style.SUCCESS('Clearing existing data...'))
        User.objects.all().delete()  # Clear users (be careful with this in production)

        # 2. Create users
        self.stdout.write(self.style.SUCCESS('Seeding the database with users...'))

        users_data = [
            {'username': 'admin', 'password': 'Password123!', 'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True},
            {'username': 'user1', 'password': 'Password123!', 'email': 'user1@example.com', 'is_staff': False, 'is_superuser': False},
            {'username': 'user2', 'password': 'Password123!', 'email': 'user2@example.com', 'is_staff': False, 'is_superuser': False},
        ]

        for user_data in users_data:
            try:
                user = User.objects.create_user(**user_data)  # Create user
                self.stdout.write(self.style.SUCCESS(f'User {user.username} created'))
            except IntegrityError:
                self.stdout.write(self.style.ERROR(f'User {user_data["username"]} already exists'))

        # 3. Seed other models with data
        # self.stdout.write(self.style.SUCCESS('Seeding other models with data...'))
        # YourModel.objects.create(name='Example Item', description='This is a test item.')
        # self.stdout.write(self.style.SUCCESS('Example item created'))

        self.stdout.write(self.style.SUCCESS('Database setup and seeding complete!'))
