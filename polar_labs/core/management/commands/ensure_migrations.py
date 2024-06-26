from io import StringIO

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
	help = 'Ensure makemigrations was run.'

	def handle(self, *args, **options):
		# This is very simple, just calling makemigrations --dry-run, we can make this smarter!

		with StringIO() as out:
			try:
				args = ['--dry-run']
				args.extend(settings.PROJECT_APPS)
				call_command('makemigrations', *args, stdout=out, stderr=out)

			except CommandError as e:
				if "run 'python manage.py makemigrations --merge'" in str(e):
					raise Exception from e(
						f'Conflict in migration files, run "python manage.py makemigrations --merge" \n'
						f'Output was: {e}',
						e,
					)

			if 'No changes detected' not in out.getvalue().strip():
				raise Exception(
					f'Missing migration files, did you forget to run makemigrations and commit the migration files? \n'
					f'Output was: {out.getvalue()}'
				)

			else:
				print('Migrations look ok')
