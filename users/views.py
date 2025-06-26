from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm,RegisterForm,UserUpdate,ProfileUpdate,LoginForm
# Create your views here.
# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request,f'Account Created..Log in to Continue')
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request,'users/register.html',{'form':form,'title':'Register'})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            messages.success(request,f'Account Created..Log in to Continue')
            
            from django.contrib.auth.models import User
            User.objects.create_user(username=username,password=password,email=email)
            
            return redirect('login') 
    else:
        form = RegisterForm()
    return render(request,'users/register.html',{'form':form,'title':'Register'})

def CustomLoginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                messages.success(request,f'Login Successful.Welcome {username}')
                login(request,user)
                return redirect('blog-home')
                
            else:
                form.add_error(None,'Invalid Username or Password')
    else:
        form = LoginForm()
    return render(request,'users/login.html',{'form':form})

def CustomLogoutView(request):
    if request.method=='POST':
        logout(request)
        return redirect('logout')
    return render(request,'users/logout.html')

# @login_required
# def profile(request):
#     if request.method=='POST':
#         u_form = UserUpdateForm(request.POST,instance=request.user)
#         p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request,f'Account Info Updated')
#             return redirect('profile')
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)
#     context = {
#         'u_form':u_form,
#         'p_form':p_form,
#     }
#     return render(request,'users/profile.html',context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdate(request.POST)
        p_form = ProfileUpdate(request.POST,request.FILES)    
        if u_form.is_valid() and p_form.is_valid():
            request.user.username = u_form.cleaned_data.get('username')
            request.user.email = u_form.cleaned_data.get('email')
            request.user.save()
            
            if p_form.cleaned_data.get('image'):
                request.user.profile.image = p_form.cleaned_data.get('image')
                request.user.profile.save()
                
            messages.success(request, 'Account Info Updated!')
            return redirect('profile')
    else:
        u_form = UserUpdate(initial={
            'username':request.user.username,
            'email':request.user.email
        })
        p_form = ProfileUpdate()
    context = {
        'u_form':u_form,
        'p_form':p_form,
    }
    return render(request,'users/profile.html',context)