from django.urls import path

from blog import views

urlpatterns = [
	path('', views.BlogPostList.as_view()),
	path('suggested-posts/', views.SuggestedBlogPostList.as_view()),
	path('tags/', views.BlogPostTagList.as_view()),
	path('<str:slug>/', views.BlogPostDetail.as_view()),
]
