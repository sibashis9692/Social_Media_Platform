from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from rest_framework import routers

urlpatterns = [

    # This two url endpoints are for jwt token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # For Authentication
    path('login/', userLoginViews.as_view(), name = "userLoginViews"),
    path('register/', userRegisterViews.as_view(), name = "userRegisterViews"),

    # This is the home page for every user
    path('home/', allPosts.as_view(), name = "allPosts"),

    # For user posts
    path('posts/', userPost.as_view(), name = "userPost"),
    path('post/delete/<int:pk>/', deletePost.as_view(), name = "deletePost"),

    # This endpoints are for seeing all your comments on different post
    path('comments/', userCommentsViews.as_view(), name = "userCommentsViews"),

    # This is for do commenst for post
    path('comment/<int:pk>/', single_commentViewer.as_view(), name = "single_commentViewer"),

    # This is for see all the comments for a specific post
    path('comments/<int:post_id>/', commentsViewer.as_view() , name='comments_view'),

    # THis is for do like for the post
    path('like/<int:pk>/', likesViewer.as_view(), name = "likesViewer"),

    # THis is for making friends
    path('follow/<str:username>/', userconnectionViewer.as_view(), name = "userconnection_View"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
