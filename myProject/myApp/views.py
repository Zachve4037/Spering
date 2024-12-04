from django.shortcuts import render
from .models import Post


#posted = [
#	{'id': 1, 'title': 'First Post', 'content': 'This is the first post'},
#	{'id': 2, 'title': 'Second Post', 'content': 'This is the second post'},
#	{'id': 3, 'title': 'Third Post', 'content': 'This is the third post'},
#]

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