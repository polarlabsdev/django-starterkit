import readtime
from autoslug import AutoSlugField
from core.base_models import BaseModel
from core.utils.cms import cms_image_preview
from django.conf import settings
from django.db import models
from django.utils.html import strip_tags

# make sure this matches $auto-colors in src/lib/styles/partials/_variables.scss
# in the polar-labs-website repo
TAG_COLOURS = {
	'surface-default': 'Surface Default',
	'surface-alt': 'Surface Alt',
	'dark-blue': 'Dark Blue',
	'dark': 'Dark',
	'darker': 'Darker',
	'grey': 'Grey',
	'light-grey': 'Light Grey',
	'primary': 'Primary',
	'secondary': 'Secondary',
	'tertiary': 'Tertiary',
	'white': 'White',
}


class BlogPostTag(BaseModel):
	name = models.CharField(null=False, blank=False, max_length=128, unique=True)
	slug = AutoSlugField(populate_from='name', editable=True, blank=True, unique=True)
	color = models.CharField(
		null=False, blank=False, max_length=24, choices=TAG_COLOURS, default='primary'
	)

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name


class BlogPost(BaseModel):
	name = models.CharField(null=False, blank=False, max_length=256, unique=True)
	slug = AutoSlugField(populate_from='name', editable=True, blank=True, unique=True)
	summary = models.CharField(null=False, blank=True, max_length=256)
	content = models.TextField(null=False, blank=False)
	tags = models.ManyToManyField(BlogPostTag, related_name='posts')
	thumbnail = models.FileField(null=False, blank=False, upload_to=settings.S3_BLOG_DIR)
	banner = models.FileField(null=False, blank=False, upload_to=settings.S3_BLOG_DIR)
	read_time = models.CharField(null=True, blank=True, max_length=24)

	def __str__(self):
		return self.name

	def banner_preview(self):
		return cms_image_preview(self.banner)

	def banner_preview_thumb(self):
		return cms_image_preview(self.banner, tiny=True)

	def thumbnail_preview(self):
		return cms_image_preview(self.thumbnail)

	def thumbnail_preview_thumb(self):
		return cms_image_preview(self.thumbnail, tiny=True)

	class Meta:
		ordering = ['-created']

	def save(self, *args, **kwargs):
		# truncate the main content to 22 words and add ... at the end
		# if we haven't set a summary ourselves
		if not self.summary:
			self.summary = ' '.join(strip_tags(self.content).split()[:22]) + '...'

		self.read_time = readtime.of_html(self.content)

		super().save(*args, **kwargs)

	@classmethod
	def get_suggested_posts(cls, related_post=None):
		"""
		A simple function for now that returns the most recent 3 posts.
		In the future we will make this smarter, but we have so little content
		right now it's not juice worth the squeeze at the moment. For now
		passing a related_post just ensures it doesn't show in the results, though
		in the future we can use it to select actual related posts.

		Args:
			related_post (BlogPost, optional): Base the results on this blog post. Defaults to None.

		Returns:
			QuerySet: A QuerySet containing 3 suggested posts
		"""
		posts = cls.objects.all()

		if related_post:
			posts = posts.exclude(pk=related_post.pk)

		return posts.order_by('-created')[:3]
