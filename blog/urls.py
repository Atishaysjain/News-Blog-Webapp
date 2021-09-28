from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('api/', views.apiOverview, name="api-overview"),
	path('post-list/', views.postList, name="api-post-list"),
	path('post-detail/<int:pk>/', views.postDetail, name="api-post-detail"),
	path('post-create/', views.postCreate, name="api-post-create"),
	path('post-update/<int:pk>/', views.postUpdate, name="api-post-update"),
	path('post-delete/<int:pk>/', views.postDelete, name="api-post-delete"),
]