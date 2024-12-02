from django.shortcuts import render

def home(request):
	context={}
	return render(request, "myApp/index.html", context)

def about(request):
	context={}
	return render(request, "myApp/about.html", context)

def category(request):
	context={}
	return render(request, "myApp/category.html", context)