from core.base_tests import BaseUnitTest

from blog.models import BlogPost


class TestModels(BaseUnitTest):
	fixtures = ['test_data.json']

	def test_get_suggested_posts_all(self):
		"""
		Check that the get_suggested_posts class method returns the expected posts
		"""
		print('TESTING get_suggested_posts...')

		expected_posts = BlogPost.objects.all().order_by('-created')[:3]
		suggested_posts = BlogPost.get_suggested_posts()

		self.assertQuerySetEqual(expected_posts, suggested_posts)

	def test_get_suggested_posts_with_post(self):
		"""
		Check that the get_suggested_posts class method doesn't include the post referenced
		"""
		print('TESTING get_suggested_posts with related post...')

		related_post = BlogPost.objects.first()

		expected_posts = BlogPost.objects.all().exclude(pk=related_post.pk).order_by('-created')[:3]
		suggested_posts = BlogPost.get_suggested_posts(related_post)

		self.assertQuerySetEqual(expected_posts, suggested_posts)
