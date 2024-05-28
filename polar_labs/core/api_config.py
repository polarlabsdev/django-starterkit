from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageBasedPagination(PageNumberPagination):
	page_size = 24
	page_size_query_param = 'page_size'
	max_page_size = 100
	page_query_param = 'page'

	def get_paginated_response(self, data):
		return Response(
			{
				'next': self.page.next_page_number() if self.page.has_next() else None,
				'previous': self.page.previous_page_number() if self.page.has_previous() else None,
				'count': self.page.paginator.count,
				'results': data,
			}
		)


class MultipleFieldLookupMixin:
	"""
	Apply this mixin to any view or viewset to get multiple field filtering
	based on a `lookup_fields` attribute, instead of the default single field filtering.
	"""

	def get_object(self):
		queryset = self.get_queryset()  # Get the base queryset
		queryset = self.filter_queryset(queryset)  # Apply any filter backends
		filter = {}

		for field in self.lookup_fields:
			if self.kwargs.get(field):  # Ignore empty fields.
				filter[field] = self.kwargs[field]

		obj = get_object_or_404(queryset, **filter)  # Lookup the object
		self.check_object_permissions(self.request, obj)
		return obj
