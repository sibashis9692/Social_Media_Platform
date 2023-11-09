from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from rest_framework import routers

urlpatterns = [

    # These two URL endpoints are for JWT token.
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # For authentication.
    path('login/', userLoginViews.as_view(), name = "userLoginViews"),
    path('register/', userRegisterViews.as_view(), name = "userRegisterViews"),

    # This is the homepage for every user.
    path('home/', allPosts.as_view(), name = "allPosts"),

    # For user posts
    path('posts/', userPost.as_view(), name = "userPost"),
    path('post/delete/<int:pk>/', deletePost.as_view(), name = "deletePost"),

    # These endpoints are for viewing all your comments on different posts.
    path('comments/', userCommentsViews.as_view(), name = "userCommentsViews"),

    # This is for commenting on posts.
    path('comment/<int:pk>/', single_commentViewer.as_view(), name = "single_commentViewer"),

    # This is for viewing all the comments for a specific post.
    path('comments/<int:post_id>/', commentsViewer.as_view() , name='comments_view'),

    # This is for liking a post.
    path('like/<int:pk>/', likesViewer.as_view(), name = "likesViewer"),

    # This is for making friends.
    path('follow/<str:username>/', userconnectionViewer.as_view(), name = "userconnection_View"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
