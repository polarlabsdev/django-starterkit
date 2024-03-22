from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates an admin user non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument('--username', required=True, help="Admin's username")
        parser.add_argument('--password', required=True, help="Admin's password")

    def handle(self, *args, **options):
        User = get_user_model()

        if not User.objects.filter(username=options['username']).exists():
            User.objects.create_superuser(
                username=options['username'], password=options['password']
            )

            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully added superuser "%s"' % options['username']
                )
            )

        else:
            self.stdout.write('Superuser "%s" already exists' % options['username'])