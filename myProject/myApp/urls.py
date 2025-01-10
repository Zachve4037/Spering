from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("category", views.category, name="category"),
    path("posts", views.posts, name="posts"),
    path("work", views.work, name="work"),
    path("createPost", views.createPost, name="createPost"),
    path("updatePost/<str:pk>/", views.updatePost, name="updatePost"),
    path("deletePost/<str:pk>/", views.deletePost, name="deletePost"),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]