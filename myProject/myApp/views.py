from gc import get_objects
from http.client import HTTPResponse
from django.contrib.messages.context_processors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.urls import reverse

def loginPage(request):
    if request.user.is_authenticated:
        return JsonResponse({'success': True, 'redirect_url': reverse('home')})

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'redirect_url': reverse('home')})
        else:
            return JsonResponse({'success': False, 'error': 'Username or password is incorrect'})

    return render(request, 'myApp/login_register.html', {'page': 'login'})

def logoutUser(request):
	logout(request)
	return redirect('home')


def registerPage(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Account created successfully')
			return redirect('login')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = UserCreationForm()

	return render(request, 'myApp/login_register.html', {'form': form})

def posts(request):
	posted = Post.objects.all()
	context = {'posts': posted}
	return render(request, "myApp/posts.html", context)

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author_name = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'myApp/post_detail.html', {'post': post, 'form': form, 'comments': comments})

def home(request):
	context={}
	return render(request, "myApp/index.html", context)

def about(request):
	context={}
	return render(request, "myApp/about.html", context)

def category(request):
	context={}
	return render(request, "myApp/category.html", context)

def work(request):
	context={}
	return render(request, 'myApp/work.html', context)

@login_required(login_url='login')
def createPost(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author_name = request.user
            post.save()
            form.save_m2m()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    else:
        form = PostForm()
    return render(request, 'myApp/post_form.html', {'form': form})

@login_required(login_url='login')
def updatePost(request, pk):
	post = Post.objects.get(id=pk)
	form = PostForm(instance=post)

	if request.user != post.author_name and not request.user.is_superuser and request.user.profile.role != 'admin':
		return HTTPResponse('You are not allowed to edit this post')

	if request.method == 'POST':
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			form.save()
			return redirect('posts')

	return render(request, 'myApp/post_form.html', {'form':form})

@login_required(login_url='login')
def deletePost(request, pk):
	post = Post.objects.get(id=pk)

	if request.user != post.author_name and not request.user.is_superuser and request.user.profile.role != 'admin':
		return HTTPResponse('You are not allowed to edit this post')

	if request.method == 'POST':
		post.delete()
		return  redirect('posts')
	return render(request, 'myApp/delete.html', {'obj':post})