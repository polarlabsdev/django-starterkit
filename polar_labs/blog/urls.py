from blog import views
from django.urls import path

urlpatterns = [
	path('', views.BlogPostList.as_view()),
	path('tags', views.BlogPostTagList.as_view()),
	path('<int:id>', views.BlogPostDetail.as_view()),
	path('<int:id>/<str:slug>', views.BlogPostDetail.as_view()),
]
