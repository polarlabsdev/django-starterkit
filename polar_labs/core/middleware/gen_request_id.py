import logging

import sentry_sdk

from core.utils import generate_request_id


class RequestLogMiddleware:
	def __init__(self, get_response):
		# One-time configuration and initialization.
		self.get_response = get_response

	def __call__(self, request):
		# Get request ID and it in sentry context
		# TODO: log request id on all requests, maybe get it from header (use nginx $request_id)
		request_id = generate_request_id()

		with sentry_sdk.configure_scope() as scope:
			scope.set_tag('request_id', request_id)

		logging.info(f'Start {request.method} Request to {request.path} with ID: {request_id}')

		return self.get_response(request)
