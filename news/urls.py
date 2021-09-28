from django.urls import path
from . import views


urlpatterns = [
    path('', views.news_page, name='news-news_page'),
    path('next', views.loadcontent, name="Loadcontent")
]