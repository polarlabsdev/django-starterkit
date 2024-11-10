from core.base_tests import LiveApiTestCase

from blog.models import BlogPost


class BlogEndpointTests(LiveApiTestCase):
	fixtures = ['test_data.json']

	# -------------------------------------------------------------------
	# REUSABLE UTILS
	# -------------------------------------------------------------------
	def _serialize_date(self, date_obj):
		# DRF does this thing with the Z for some reason
		# https://github.com/encode/django-rest-framework/blob/36d5c0e74f562cbe3055f0d20818bd48d3c32359/rest_framework/fields.py#L1212C25-L1212C41
		return date_obj.isoformat()[:-6] + 'Z'

	def _check_tags(self, tags_queryset, tags_response):
		for i, tag in enumerate(tags_queryset.all()):
			self.assertEqual(tag.name, tags_response[i]['name'])
			self.assertEqual(tag.slug, tags_response[i]['slug'])
			self.assertEqual(tag.color, tags_response[i]['color'])

	def _check_list_post(self, db_post, response_post):
		self.assertEqual(db_post.name, response_post['name'])
		self.assertEqual(db_post.summary, response_post['summary'])
		self.assertEqual(db_post.thumbnail.url, response_post['thumbnail'])
		self.assertEqual(db_post.read_time, response_post['read_time'])
		self.assertEqual(db_post.slug, response_post['slug'])

		# DRF does this thing with the Z for some reason
		# https://github.com/encode/django-rest-framework/blob/36d5c0e74f562cbe3055f0d20818bd48d3c32359/rest_framework/fields.py#L1212C25-L1212C41
		self.assertEqual(self._serialize_date(db_post.created), response_post['created'])
		self._check_tags(db_post.tags, response_post['tags'])

	def _check_suggested_posts(self, s_posts_queryset, s_posts_response):
		for i, post in enumerate(s_posts_queryset.all()):
			self._check_list_post(post, s_posts_response[i])

	# -------------------------------------------------------------------
	# TEST FUNCS
	# -------------------------------------------------------------------
	def test_blog_list(self):
		"""
		Make a request to the API and ensure we get a response from the list blog posts endpoint
		"""
		print('INTEG TESTING BLOG LIST ENDPOINT...')

		response = self.get('blog/')

		db_count = BlogPost.objects.count()
		self.assertGreater(db_count, 0)  # verify test data exists
		self.assertEqual(response['count'], db_count)  # verify response count

		first_db_post = BlogPost.objects.first()
		first_response_post = response['results'][0]

		self._check_list_post(first_db_post, first_response_post)

	def test_blog_detail(self):
		"""
		Make a request to the API and ensure we get the correct response from the blog post detail endpoint
		"""
		print('INTEG TESTING BLOG POST DETAIL ENDPOINT...')

		test_post = BlogPost.objects.first()
		suggested_posts = BlogPost.get_suggested_posts(test_post)

		response = self.get(f'blog/{test_post.slug}')

		self.assertEqual(test_post.name, response['name'])
		self.assertEqual(test_post.content, response['content'])
		self.assertEqual(test_post.banner.url, response['banner'])
		self.assertEqual(self._serialize_date(test_post.created), response['created'])

		self._check_suggested_posts(suggested_posts, response['suggested_posts'])
		self._check_tags(test_post.tags, response['tags'])
