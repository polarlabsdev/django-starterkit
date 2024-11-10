from core.base_admin import BaseAdmin
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from blog.models import BlogPost, BlogPostTag


@admin.register(BlogPostTag)
class BlogPostTagAdmin(BaseAdmin):
	list_display = [
		'id',
		'name',
		'slug',
		'color',
		'created',
		'updated',
	]

	fields = [
		'id',
		'name',
		'slug',
		'color',
		('created', 'updated'),
	]

	search_fields = ['name']
	list_display_links = ('id', 'name')
	readonly_fields = ['id', 'created', 'updated']


class BlogPostTagInline(admin.TabularInline):
	model = BlogPost.tags.through
	verbose_name = 'Blog Tag'
	verbose_name_plural = 'Blog Tags'


@admin.register(BlogPost)
class BlogPostAdmin(BaseAdmin, SummernoteModelAdmin):
	list_display = [
		'id',
		'thumbnail_preview_thumb',
		'name',
		'slug',
		'get_tags',
		'read_time',
		'created',
		'updated',
	]

	fields = [
		'id',
		'name',
		'slug',
		'summary',
		'content',
		'read_time',
		'banner',
		'banner_preview',
		'thumbnail',
		'thumbnail_preview',
		('created', 'updated'),
	]

	inlines = [BlogPostTagInline]
	search_fields = ['name', 'summary', 'content']
	list_filter = ['tags__name']
	readonly_fields = (
		'id',
		'created',
		'updated',
		'banner_preview',
		'thumbnail_preview',
		'read_time',
	)
	summernote_fields = ('content',)
	list_display_links = ('id', 'thumbnail_preview_thumb', 'name')

	def get_tags(self, obj):
		tags = ', '.join([tag.name for tag in obj.tags.all()])
		return tags
