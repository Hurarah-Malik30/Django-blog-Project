from django.contrib import admin
from django.urls import path,include
from .views import CustomPostCreate,CustomPostUpdate,CustomPostListView,CustomUserPostListView,CustomDetailPostView,CustomPostDeleteView
from . import views

urlpatterns = [
   path('',CustomPostListView,name='blog-home'),
   path('user/<str:username>',CustomUserPostListView,name='user-posts'),
   path('about/',views.about,name='blog-about'),
   path('post/<int:pk>/',CustomDetailPostView,name='post-detail'),
   path('post/new/',CustomPostCreate,name='post-create'),
   path('post/<int:pk>/update/',CustomPostUpdate,name='post-update'),
   path('post/<int:pk>/delete/',CustomPostDeleteView,name='post-delete')

]