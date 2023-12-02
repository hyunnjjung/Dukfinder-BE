from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from . import views
from .views import CategoryPostsView, LostPostListView, LostPostDetailView, ThisWeekPostsListView, \
    ThisMonthPostsListView, LostPostSearchAPIView, LostPostCreateView, LostPostUpdateView, \
    CommentViewSet, ReplyViewSet

urlpatterns = [
    path('lost_posts/', LostPostListView.as_view(), name='post-list'),
    path('lost_posts/<int:pk>/', LostPostDetailView.as_view(), name='post-detail'),
    path('lost_posts/create/', LostPostCreateView.as_view(), name='post-create'),
    path('lost_posts/<int:intLpk>/update/', LostPostUpdateView.as_view(), name='post-update'),
    path('lost_posts/this-week/', ThisWeekPostsListView.as_view(), name='this-week-posts-list'),
    path('lost_posts/this-month/', ThisMonthPostsListView.as_view(), name='this-month-posts-list'),
    path('lost_posts/category/<str:category>', CategoryPostsView.as_view(), name='category-posts'),
    path('lost_posts/search/', LostPostSearchAPIView.as_view(), name='post-search-api'),
    path('lost_posts/<int:pk>/comment/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comment-list'),
    path('lost_posts/<int:post_pk>/comment/<int:pk>/',
         CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='comment-detail'),
    path('lost_posts/<int:pk>/reply/', ReplyViewSet.as_view({'get': 'list', 'post': 'create'}), name='reply-list'),
    path('lost_posts/<int:post_pk>/reply/<int:pk>/', ReplyViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='reply-detail'),
]
