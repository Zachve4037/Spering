# myApp/urls.py
from django.contrib.admindocs.utils import docutils_is_available
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('category/', views.category, name='category'),
    path('work/', views.work, name='work'),
    path('posts/', views.posts, name='posts'),
    path('category/<int:category_id>/', views.category_page, name='category_page'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create_post/', views.create_post, name='create_post'),  # Ensure this name matches
    path('update_post/<int:pk>/', views.update_post, name='update_post'),
    path('delete_post/<int:pk>/', views.deletePost, name='delete_post'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)