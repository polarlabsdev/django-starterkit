import os
from pathlib import Path
import re

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Ensure tests follow unittest discovery requirements.'

    def handle(self, *args, **options):
        for root, dirs, files in os.walk(settings.BASE_DIR, topdown=True):
            # skip special folders
            for d in list(dirs):
                if re.search(r'(^\.|fixtures?|resources|migrations|static|__py)', d):
                    dirs.remove(d)

            # if this is not the root, there must be an __init__
            if not root == settings.BASE_DIR:
                if '__init__.py' not in files:
                    raise ValueError(f'No init file found in {root}')

            # ensure the file names follow the unittest pattern
            for file_name in files:
                if re.search(r'.*test.*\.py$', file_name, re.I) and not re.search(
                    r'^test.*\.py$', file_name
                ):
                    # except for some commands
                    if file_name not in (
                        'ensure_tests_run.py',
                        'generate_test_jwt.py',
                        'send_test_push.py',
                    ):
                        raise ValueError(
                            f"File looks like it wants to be a test but it won't run! Must start with 'test', "
                            f"was: {root}/{file_name}'"
                        )

                if re.search(r'^test.*\.py$', file_name):
                    # ensure the method names in tests files follow the the unittest pattern and are unique
                    unique_tests = {}
                    current_class = None

                    with open(Path(root) / file_name, 'r') as f:
                        for line in f:
                            match = re.search(
                                r'class .*?(BabblyApiTestCase|IntegLiveServerTestCase|TestCase).*?\)',
                                line,
                                re.I,
                            )
                            if match:
                                current_class = match.group(0)

                                if current_class in unique_tests.keys():
                                    raise ValueError(
                                        f'The classname {current_class} has been duplicated'
                                    )

                                else:
                                    unique_tests[current_class] = set()

                            match = re.search(r'def .*?test.*?\(', line, re.I)
                            if match:
                                match = match.group(0)

                                if match in unique_tests[current_class]:
                                    raise ValueError(
                                        f"There seems to be a duplicate test method (one won't run). "
                                        f'Test: {match}. If this belongs to a different class, '
                                        f'sorry, this script is still not smart enough.'
                                    )
                                unique_tests[current_class].add(match)
                                if not re.search(r'def (_|test|setup)', line, re.I):
                                    raise ValueError(
                                        f"The method looks like a test, but it won't run! Must start with "
                                        f"'test', was: {line}. If this is not meant to be a test you can make it start "
                                        f"with '_'"
                                    )

        print('Looks like tests will run.')