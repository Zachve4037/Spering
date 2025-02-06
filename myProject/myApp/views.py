from http.client import HTTPResponse
from django.contrib  import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Genre, Profile
from .forms import PostForm, CommentForm, AvatarUploadForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseNotFound
from django.urls import reverse
from django.templatetags.static import static


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
            messages.success(request, 'Account created successfully!')
            return redirect('login')
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
	context={'genres': Genre.objects.all()}
	return render(request, "myApp/index.html", context)

def about(request):
	context={}
	return render(request, "myApp/about.html", context)

def category(request):
    context = {'genres': Genre.objects.all()}
    return render(request, "myApp/category.html", context)

def work(request):
	context={'genres': Genre.objects.all()}
	return render(request, 'myApp/work.html', context)

@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author_name = request.user
            post.save()
            form.save_m2m()
            return JsonResponse({'success': True, 'post_id': post.id})
        else:
            print("Form Errors:", form.errors)
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = PostForm()
    return render(request, 'myApp/post_form.html', {'form': form, 'is_update': False})


@login_required(login_url='login')
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author_name and not request.user.is_superuser and request.user.profile.role != 'admin':
        return JsonResponse({'success': False, 'error': 'You are not authorized to update this post'})

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = PostForm(instance=post)
    return render(request, 'myApp/post_form.html', {'form': form, 'is_update': True, 'post': post})


@login_required(login_url='login')
def deletePost(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponseNotFound('No Post matches the given query.')

    if request.user != post.author_name and not request.user.is_superuser and request.user.profile.role != 'admin':
        return JsonResponse({'success': False, 'error': 'You are not authorized to delete this post'})

    if request.method == 'POST':
        post.delete()
        return redirect('posts')
    return render(request, 'myApp/delete.html', {'obj': post})

def category_page(request, category_id):
    category = get_object_or_404(Genre, id=category_id)
    posts = Post.objects.filter(genres=category)
    return render(request, 'myApp/category_page.html', {'category': category, 'posts': posts})

@login_required(login_url='login')
def user_dashboard(request):
    user_author_name = request.user.id
    user_posts = Post.objects.filter(author_name_id=user_author_name)
    context = {'user_posts': user_posts}
    return render(request, 'myApp/user_dashboard.html', context)


@login_required
def dashboard(request):
    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'avatar_url': request.user.profile.avatar.url})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = AvatarUploadForm(instance=request.user.profile)

    if request.user.profile.avatar:
        avatar_url = request.user.profile.avatar.url
    else:
        avatar_url = static('images/default-avatar.jpg')

    print(f"DEBUG: User Avatar = {request.user.profile.avatar}")
    print(f"DEBUG: Avatar URL = {avatar_url}")

    return render(request, 'myApp/user_dashboard.html', {
        'form': form,
        'user_posts': Post.objects.filter(author_name=request.user),
        'avatar_url': avatar_url
    })


@login_required
def upload_avatar(request):
    if request.method == 'POST':
        if 'avatar' not in request.FILES:
            return JsonResponse({'success': False, 'error': 'No file received'})

        profile = request.user.profile
        form = AvatarUploadForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            print("Saved Avatar Path:", profile.avatar.url)
            return JsonResponse({'success': True, 'avatar_url': profile.avatar.url})
        else:
            print("Form Errors:", form.errors)
            return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

def custom_404(request, exception):
    return render(request, '404.html', {}, status=404)

@login_required
def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author_name:
        return redirect('post_detail', post_id=comment.post.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'myApp/update_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author_name:
        comment.delete()
    return redirect('post_detail', post_id=comment.post.id)