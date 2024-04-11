from blog.models import BlogPost, BlogPostTag
from blog.serializers import BlogPostSerializer, BlogPostTagSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView


# https://www.django-rest-framework.org/api-guide/generic-views/#genericapiview
class BlogPostList(ListAPIView):
	queryset = BlogPost.objects.all()
	serializer_class = BlogPostSerializer


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
