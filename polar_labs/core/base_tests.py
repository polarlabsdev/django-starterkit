from pprint import pformat

import requests
from django.test import LiveServerTestCase, TestCase


# This class is empty for now as there's nothing really to add to a
# global unit test case just yet, but creating it anyways so we can
# inherit it from it in all our unit tests and if we decide to add
# something later we don't need to find all the unit tests and adjust
# them - can just start adding things.
class BaseUnitTest(TestCase):
	def setUp(self):
		print('\n--------\n')

	def tearDown(self):
		print('\n--------\n')


# This class is a utility class we created that extends the built-in
# Django LiveServerTestCase. We added an ability to use an external url
# to run the same tests against a live server and a number of convenience
# methods that need to run on all api tests (like don't be an error code
# unless we expect an error code).
class LiveApiTestCase(LiveServerTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()

		cls.test_url = cls.live_server_url

		if cls.test_url != cls.live_server_url:
			print(f'USING LIVE TEST URL: {cls.test_url}')

	def _pre_setup(self):
		super()._pre_setup()

		self.default_headers = {'Content-Type': 'application/json'}

		print('\n--------\n')

	def _post_teardown(self):
		super()._post_teardown()
		print('\n--------\n')

	def _get_url_and_headers(self, endpoint, use_auth, extra_headers):
		url = f'{self.test_url}/{endpoint}'
		headers = self.default_headers

		if use_auth:
			pass  # not implemented

		if extra_headers:
			for header, value in extra_headers.items():
				headers[header] = value

		return url, headers

	def _check_response(self, expected_error_code, response_obj):
		if not expected_error_code:
			self.assertEqual(response_obj.status_code, 200)
		else:
			self.assertEqual(response_obj.status_code, expected_error_code)

		try:
			response = response_obj.json()

		except ValueError:
			response = response_obj.content
			self.fail(f'Test failed with Django Framework error: {pformat(response)}')

		return response

	def get(self, endpoint, use_auth=True, extra_headers=None, expected_error_code=None):
		url, headers = self._get_url_and_headers(endpoint, use_auth, extra_headers)

		print(f'Sending GET request to {url}...\n')

		response_obj = requests.get(
			url,
			headers=headers,
		)

		response = self._check_response(expected_error_code, response_obj)

		return response

	# TODO: implement post, put, delete as needed
