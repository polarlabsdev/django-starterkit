from core.base_tests import LiveApiTestCase

from blog.models import BlogPost


class BlogEndpointTests(LiveApiTestCase):
	fixtures = ['test_data.json']

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

		self.assertEqual(first_db_post.id, first_response_post['id'])

	def test_blog_detail(self):
		"""
		Make a request to the API and ensure we get the correct response from the blog post detail endpoint
		"""
		print('INTEG TESTING BLOG POST DETAIL ENDPOINT...')

		test_post = BlogPost.objects.first()

		response = self.get(f'blog/{test_post.id}')
		self.assertEqual(test_post.id, response['id'])
