from core.base_admin import BaseAdmin
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from blog.models import BlogPost, BlogPostTag


@admin.register(BlogPostTag)
class BlogPostTagAdmin(BaseAdmin):
	list_display = [
		'id',
		'name',
		'created',
		'updated',
	]
	search_fields = ['tag_name']
	list_display_links = ('id', 'name')


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
		'created',
		'updated',
	]

	fields = [
		'id',
		'name',
		'slug',
		'content',
		'banner',
		'banner_preview',
		'thumbnail',
		'thumbnail_preview',
		('created', 'updated'),
	]

	inlines = [BlogPostTagInline]
	search_fields = ['name', 'content']
	readonly_fields = (
		'id',
		'created',
		'updated',
		'banner_preview',
		'thumbnail_preview',
		'slug',
	)
	summernote_fields = ('content',)
	list_display_links = ('id', 'thumbnail_preview_thumb', 'name')
