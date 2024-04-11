from blog.models import BlogPost, BlogPostTag
from rest_framework.serializers import ModelSerializer


class BlogPostTagSerializer(ModelSerializer):
	class Meta:
		model = BlogPostTag
		fields = [
			'id',
			'name',
		]


class BlogPostSerializer(ModelSerializer):
	tags = BlogPostTagSerializer(many=True, read_only=True)

	class Meta:
		model = BlogPost
		fields = [
			'id',
			'name',
			'slug',
			'content',
			'tags',
			'banner',
			'thumbnail',
		]
