from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import PostSerializer
from rest_framework.permissions import IsAdminUser

@api_view(['GET'])
@permission_classes([IsAdminUser])
def apiOverview(request):
	api_urls = {
		'List':'/api-post-list/',
		'Detail View':'/api-post-detail/<str:pk>/',
		'Create':'/api-post-create/',
		'Update':'/api-post-update/<str:pk>/',
		'Delete':'/api-post-delete/<str:pk>/',
		}

	return Response(api_urls)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def postList(request):
	posts = Post.objects.all().order_by('-id')
	serializer = PostSerializer(posts, many=True)
	return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def postDetail(request, pk):
	posts = Post.objects.get(id=pk)
	serializer = PostSerializer(posts, many=False)
	return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def postCreate(request):
	serializer = PostSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def postUpdate(request, pk):
	post = Post.objects.get(id=pk)
	serializer = PostSerializer(instance=post, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def postDelete(request, pk):
	post = Post.objects.get(id=pk)
	post.delete()

	return Response('Item succsesfully delete!')

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username')) # Getting user from url
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):  # Uses post_form.html
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False