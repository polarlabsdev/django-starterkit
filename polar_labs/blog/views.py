from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from blog.models import BlogPost, BlogPostTag
from blog.serializers import BlogPostDetailSerializer, BlogPostListSerializer, BlogPostTagSerializer


# https://www.django-rest-framework.org/api-guide/generic-views/#genericapiview
class BlogPostList(ListAPIView):
	queryset = BlogPost.objects.all()
	serializer_class = BlogPostListSerializer
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
	filterset_fields = {'tags__slug': ['in', 'icontains']}
	search_fields = ['name', 'summary', 'content']
	ordering_fields = ['name', 'created', 'updated']


class BlogPostTagList(ListAPIView):
	queryset = BlogPostTag.objects.all()
	serializer_class = BlogPostTagSerializer


# just looking up by pk in case the title of the blog post changes for some reason
# that would invalidate anyone's bookmarks or similar.
class BlogPostDetail(RetrieveAPIView):
	queryset = BlogPost.objects.all()
	serializer_class = BlogPostDetailSerializer
	lookup_field = 'slug'
	lookup_url_kwarg = 'slug'


class SuggestedBlogPostList(ListAPIView):
	serializer_class = BlogPostListSerializer

	def get_queryset(self):
		return BlogPost.get_suggested_posts()
