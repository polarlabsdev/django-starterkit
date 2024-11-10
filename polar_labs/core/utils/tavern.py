import os
import time

from jsonschema import validate


# a common JSONSchema base generator for integration tests that ensures the
# props we pass are actually required (really dumb they aren't by defualt)
def gen_obj_schema_definition(expected_props):
	return {
		'type': 'object',
		'properties': expected_props,
		'required': [key for key in expected_props],
		'additionalProperties': False,
	}


# There is currently no retry backoff param in tavern, so this is a hack to
# cause a backoff manually. The idea is that we check the response status code,
# and if it's a code that merits a retry, we sleep for our backoff time and then
# raise an error that fails the step and triggers an immediate retry from tavern.
# We don't trigger the retry here as there is no mechanism for that, the idea is
# to fail the test so tavern will retry - the trick is to sleep for a period before
# failing the test.
class RetryException(Exception):
	pass


def check_response(response, schema):
	if response.status_code in [502, 503, 504, 408]:
		time.sleep(int(os.environ.get('RETRY_BACKOFF', 5)))  # default to 5 if no env var
		raise RetryException()

	validate(instance=response.json(), schema=schema)
