from http.client import HTTPResponse

from django.contrib.messages.context_processors import messages
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from .forms import PostForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


#posted = [
#	{'id': 1, 'title': 'First Post', 'content': 'This is the first post'},
#	{'id': 2, 'title': 'Second Post', 'content': 'This is the second post'},
#	{'id': 3, 'title': 'Third Post', 'content': 'This is the third post'},
#]

def loginPage(request):
	page = 'login'
	context = {'page': page}
	if request.user.is_authenticated:
		return redirect('home')

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			context['error'] = 'User does not exist'
			return render(request, 'myApp/login_register.html', context)

		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.error(request, 'Username or password is incorrect')

	return render(request, 'myApp/login_register.html', context)

def logoutUser(request):
	logout(request)
	return redirect('home')

def registerPage(request):
	form = UserCreationForm()
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			form.save()
			login(request, user)
			return redirect('home')
		else:
			messages.error(request, 'An error has occurred during registration')
	return render(request, 'myApp/login_register.html', {'form': form})

def posts(request):
	posted = Post.objects.all()
	context = {'posts': posted}
	return render(request, "myApp/posts.html", context)

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
			return redirect('posts')
	else:
		form = PostForm()

	context={'form': form}
	return render(request, "myApp/post_form.html", context)

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