from django.db import models
from core.base_models import BaseModel
from django.conf import settings
from core.utils.cms import cms_image_preview
from autoslug import AutoSlugField


class BlogPostTag(BaseModel):
  name = models.CharField(null=False, blank=False, max_length=128, unique=True)

  def __str__(self):
    return self.name 

class BlogPost(BaseModel):
  name = models.CharField(null=False, blank=False, max_length=256)
  slug = AutoSlugField(populate_from='name')
  content = models.TextField(null=False, blank=False)
  tags = models.ManyToManyField(BlogPostTag, related_name='tags')
  banner = models.FileField(null=False, blank=False, upload_to=settings.S3_BLOG_DIR)
  thumbnail = models.FileField(null=False, blank=False, upload_to=settings.S3_BLOG_DIR)

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
    ordering = ['updated']