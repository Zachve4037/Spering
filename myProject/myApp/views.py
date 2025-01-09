from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth.models import User


#posted = [
#	{'id': 1, 'title': 'First Post', 'content': 'This is the first post'},
#	{'id': 2, 'title': 'Second Post', 'content': 'This is the second post'},
#	{'id': 3, 'title': 'Third Post', 'content': 'This is the third post'},
#]

def loginPage(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            context['error'] = 'User does not exist'
            return render(request, 'myApp/login_register.html', context)

    return render(request, 'myApp/login_register.html', context)

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

def createPost(request):
	form = PostForm()
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('posts')

	context={'form': form}
	return render(request, "myApp/post_form.html", context)

def updatePost(request, pk):
	post = Post.objects.get(id=pk)
	form = PostForm(instance=post)

	if request.method == 'POST':
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			form.save()
			return redirect('posts')

	return render(request, 'myApp/post_form.html', {'form':form})

def deletePost(request, pk):
	post = Post.objects.get(id=pk)
	if request.method == 'POST':
		post.delete()
		return  redirect('posts')
	return render(request, 'myApp/delete.html', {'obj':post})