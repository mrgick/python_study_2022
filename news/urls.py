from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/<int:news_id>/', views.news_item, name='news item'),
    path('news/add/', views.news_item_add, name='news add'),
    path('news/<int:news_id>/edit/', views.news_item_edit, name='news edit'),
    path('news/<int:news_id>/delete/',
         views.news_item_delete,
         name='news delete'),
    path('blogs/', views.all_blogs, name='blogs list'),
    path('blog/<int:blog_id>/', views.news_from_blog, name='blog news'),
    path('blog/add/', views.blog_item_add, name='blog add'),
]
