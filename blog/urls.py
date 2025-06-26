from django.contrib import admin
from django.urls import path,include
from .views import PostListView,PostDetailView,PostDeleteView,UserPostListView,CustomPostCreate,CustomPostUpdate
from . import views

urlpatterns = [
   path('',PostListView.as_view(),name='blog-home'),
   path('user/<str:username>',UserPostListView.as_view(),name='user-posts'),
   path('about/',views.about,name='blog-about'),
   path('post/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
   path('post/new/',CustomPostCreate,name='post-create'),
   path('post/<int:pk>/update/',CustomPostUpdate,name='post-update'),
   path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='post-delete')

]