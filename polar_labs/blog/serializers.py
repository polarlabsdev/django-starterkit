from rest_framework.serializers import ModelSerializer, SerializerMethodField

from blog.models import BlogPost, BlogPostTag


class BlogPostTagSerializer(ModelSerializer):
	class Meta:
		model = BlogPostTag
		fields = ['name', 'slug', 'color']


class BlogPostListSerializer(ModelSerializer):
	tags = BlogPostTagSerializer(many=True, read_only=True)

	class Meta:
		model = BlogPost
		fields = [
			'name',
			'slug',
			'summary',
			'tags',
			'thumbnail',
			'read_time',
			'created',
			'updated',
		]


class BlogPostDetailSerializer(ModelSerializer):
	tags = BlogPostTagSerializer(many=True, read_only=True)
	suggested_posts = SerializerMethodField()

	class Meta:
		model = BlogPost
		fields = [
			'name',
			'slug',
			'summary',
			'content',
			'tags',
			'banner',
			'created',
			'updated',
			'suggested_posts',
		]

	def get_suggested_posts(self, obj):
		posts = BlogPost.get_suggested_posts(obj)
		serializer = BlogPostListSerializer(posts, many=True)

		return serializer.data
