from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import PostCreate,PostUpdate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
# Create your views here.
 

def about(request):
    return render(request,'blog/about.html',{'title': 'About'})

def CustomPostListView(request):
    posts = Post.objects.all().order_by('-date_posted')
    paginator = Paginator(posts,5)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    is_paginated = page_obj.has_other_pages()
    context = {
        'posts':page_obj,
        'title': "CustomListView",
        'is_paginated':is_paginated
    }
    return render(request,'blog/home.html',context)

def CustomUserPostListView(request,username):
    user = get_object_or_404(User,username=username)
    posts = Post.objects.filter(author=user).order_by('-date_posted')
    paginator = Paginator(posts,5)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    is_paginated = page_obj.has_other_pages()
    context ={
        'title': "Custom User Posts",
        'username':user,
        'is_paginated':is_paginated,
        'posts': page_obj
    }
    return render(request,'blog/user_posts.html',context)

def CustomDetailPostView(request,pk):
    post = get_object_or_404(Post,pk=pk)
    context ={
        'title': "CustomPostforpk",
        'object':post
    }
    return render(request,'blog/post_detail.html',context)


def CustomPostDeleteView(request,pk):
    post = get_object_or_404(Post,pk=pk)
    
    if post.author != request.user:
        messages.error(request,'You are not authorised to delete this post')
        return redirect('post_detail',pk=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request,'Post Deleted Successfully.')
        return redirect('blog-home')
    
    context = {
        'post':post
    }  
    return render(request, 'blog/post_confirm_delete.html', context)
    
    
    
@login_required
def CustomPostCreate(request):
    if request.method == 'POST':
        form = PostCreate(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            author = request.user
            post = Post(title=title,content=content,author=author)
            post.save()
            return redirect('blog-home')
    else:
        form = PostCreate()
    return render(request,'blog/post_form.html',{'form':form})

def CustomPostUpdate(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = PostUpdate(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data.get('title')
            post.content = form.cleaned_data.get('content')
            post.save()
            return redirect('post-detail',pk=post.pk)
    else:
        form = PostUpdate(initial={'title': post.title, 'content': post.content})

    return render(request, 'blog/post_update.html', {'form': form})