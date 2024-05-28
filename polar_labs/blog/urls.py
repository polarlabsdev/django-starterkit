from django.urls import path

from blog import views

urlpatterns = [
	path('', views.BlogPostList.as_view()),
	path('tags/', views.BlogPostTagList.as_view()),
	path('<int:id>/', views.BlogPostDetail.as_view()),
	path('<int:id>/<str:slug>/', views.BlogPostDetail.as_view()),
	path('test-headers/', views.TestHeaders.as_view()),
]
