from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from .forms import PostCreate,PostUpdate
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    context = {
        'posts':Post.objects.all(),
        # 'title':'My Blog'
    }
    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False    

def about(request):
    return render(request,'blog/about.html',{'title': 'About'})

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