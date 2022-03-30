from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('news/<int:news_id>/', views.news_item, name='news item'),
    path('news/<int:news_id>/edit/', views.news_item_edit, name='news item editor'),
    path('blogs/',views.all_blogs, name='blogs list'),
    path('blog/<int:blog_id>/', views.news_from_blog, name='blog news'),
]
