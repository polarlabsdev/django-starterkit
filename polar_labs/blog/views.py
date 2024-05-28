from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import BlogPost, BlogPostTag
from blog.serializers import BlogPostSerializer, BlogPostTagSerializer


# https://www.django-rest-framework.org/api-guide/generic-views/#genericapiview
class BlogPostList(ListAPIView):
	queryset = BlogPost.objects.all()
	serializer_class = BlogPostSerializer
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
	filterset_fields = {'tags__slug': ['in', 'icontains']}
	search_fields = ['name', 'content']
	ordering_fields = ['name', 'created', 'updated']


class BlogPostTagList(ListAPIView):
	queryset = BlogPostTag.objects.all()
	serializer_class = BlogPostTagSerializer


# just looking up by pk in case the title of the blog post changes for some reason
# that would invalidate anyone's bookmarks or similar.
class BlogPostDetail(RetrieveAPIView):
	queryset = BlogPost.objects.all()
	serializer_class = BlogPostSerializer
	lookup_field = 'pk'
	lookup_url_kwarg = 'id'


class TestHeaders(APIView):
	def get(self, request, format=None):
		return Response(request.headers)
