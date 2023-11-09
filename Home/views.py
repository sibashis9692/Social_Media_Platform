from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializer import *
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from rest_framework.status import *

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# This is a registration view class
class userRegisterViews(CreateAPIView):
        queryset = User.objects.all()
        serializer_class = userregisterSerializer

# This is a Login view class
class userLoginViews(CreateAPIView):
    serializer_class = userloginSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data = request.data)
            if(serializer.is_valid(raise_exception = True)):
                user = User.objects.filter(email = serializer.data.get("email")).first()

                if(user is not None):
                    print(check_password(serializer.data.get("password"), user.password))
                    if(user.username != serializer.data.get("username") or not check_password(serializer.data.get("password"), user.password)):
                        return Response({"Message" : "credential is not correct"}, HTTP_400_BAD_REQUEST)
                    token = get_tokens_for_user(user)
                    return Response({"Message" : "successful", "Token" : token}, HTTP_200_OK)
                return Response({"Message" : "The user is not found."}, HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"Error" : e})
        
# Using this class, the current user can view all of their posts and create new ones.
class userPost(ListAPIView, CreateAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Posts.objects.all()
    serializer_class = userpostSerializer

    def get_queryset(self):
        user = self.request.user
        return Posts.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Using this, the current user can delete their post.
class deletePost(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            post = Posts.objects.filter(id = pk).first()

            if(post):
                if(post.user.username == request.user.username):
                    path = os.path.join(BASE_DIR, 'images', str(post.images))

                    if(os.path.exists(path)):
                        os.remove(path)

                    post.delete()
                    return Response({"Message" : "Successfully Delete"}, HTTP_200_OK)
                return Response({"Message" : "You are not an authorized person to delete the post."}, HTTP_401_UNAUTHORIZED)
            return Response({"Message" : f"No posts are available with the ID {pk}"}, HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"Error" : str(e)})
        
# Using this class, the current user can view all their comments on different posts.
class userCommentsViews(ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Comments.objects.all()
    serializer_class = usercommentsSerializer

    def get_queryset(self):
        try:
            user = self.request.user
            return Comments.objects.filter(user=user)
        except Exception as e:
            return Response({"Error" : e})
        
# This class functions as a home page where the current user can view posts from various users.
class allPosts(ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Posts.objects.all()
    serializer_class = userpostSerializer

# Using this class, the current user can like and dislike specific posts.
class likesViewer(ListAPIView, CreateAPIView, UpdateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Likes.objects.all()
    serializer_class = likesSerializer

    def get_queryset(self):
        try:
            user = self.request.user
            pk = self.kwargs.get('pk')
            post = Posts.objects.filter(id=pk).first()

            if post:
                return Likes.objects.filter(user=user, post=post)
            return Likes.objects.none()
        except Exception as e:
            return Response({"Error" : e})
        
    def post(self, request, pk, *args, **kwargs):
        try:
            post = Posts.objects.filter(id = pk).first()

            if(post):
                data = {
                    'like' : False
                }

                if "like" in request.data:
                    data['like'] = True

                like_exists = Likes.objects.filter(user = request.user, post = post).first()

                if(like_exists):
                    return Response({"Error" : f"You have already {'Like' if like_exists.like else 'DisLike'} the post"}, HTTP_400_BAD_REQUEST)
                
                serializer = likesSerializer(data = data, context={'user' : request.user, 'post' : post})
                if(serializer.is_valid(raise_exception=True)):
                    serializer.save()
                    return Response({"Message": serializer.data}, HTTP_200_OK)
                
            return Response({"Message" : "The post does not exist"}, HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"Error" : e})
        
    def put(self, request, pk, *args, **kwargs):
        try:
            post = Posts.objects.filter(id = pk).first()
            if(post):
                data = {
                    'like' : False
                }
                if "like" in request.data:
                    data['like'] = True

                like_exists = Likes.objects.filter(user = request.user, post = post).first()

                if(like_exists):
                    if(like_exists.like == data.get('like')):
                        return Response({"Arelr" : f"You have already {'Like' if like_exists.like else 'DisLike'} the post"}, HTTP_400_BAD_REQUEST)
                    
                    serializer = likesSerializer(like_exists, data = data, partial = True)
                    if(serializer.is_valid(raise_exception=True)):
                        serializer.save()
                        return Response({"Message": serializer.data}, HTTP_200_OK)
                return Response({"Message": "You have not Like yet."}, HTTP_400_BAD_REQUEST)
            return Response({"Message": "The post does not exist."}, HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"Error" : e})
        
# Using this class, the current user can leave a comment and also delete the comment on a specific post.
class single_commentViewer(ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Comments.objects.all()
    serializer_class = commentSerializer

    def get_queryset(self):
        try:
            user = self.request.user
            pk = self.kwargs.get('pk')
            post = Posts.objects.filter(id=pk).first()

            if post:
                return Comments.objects.filter(user=user, post=post)
            return Comments.objects.none()
        except Exception as e:
            return Response({"Error" : e})
        
    def post(self, request, pk):
        try:
            post = Posts.objects.filter(id = pk).first()
            if(post):
                data = {
                    'comment' : request.data["comment"]
                }

                exists_comment = Comments.objects.filter(user = request.user, post = post).first()
                if(exists_comment):
                    return Response({"Message" : "You have already commented."}, HTTP_400_BAD_REQUEST)

                serializer = commentSerializer(data = data, context = {'post' : post, 'user' : request.user})
                if(serializer.is_valid(raise_exception=True)):
                    print(serializer.validated_data)
                    serializer.save()
                    return Response({"Message": serializer.data}, HTTP_200_OK)
                
            return Response({"Message" : "The post does not exist"}, HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"Error" : e})
        
    def put(self, request, pk):
        try:
            post = Posts.objects.filter(id=pk).first()
            if post:

                exists_comment = Comments.objects.filter(user=request.user, post=post).first()
                if exists_comment:
                    # Fetch the existing comment data
                    serializer = commentSerializer(exists_comment, data=request.data, partial=True)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        return Response({"Message": serializer.data}, HTTP_200_OK)
                return Response({"Message": "You have not commented yet."}, HTTP_400_BAD_REQUEST)
            return Response({"Message": "The post does not exist"}, HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"Error" : e})

# This helps to display all comments of a single post.
class commentsViewer(ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Comments.objects.all()
    serializer_class = commentSerializer



# This helps to follow users.
class userconnectionViewer(ListAPIView, CreateAPIView):
    queryset = Connection.objects.all()
    serializer_class = conectionSerilaizer
    
    def get_queryset(self):
        try:
            user = self.request.user
            connection = Connection.objects.filter(user = user)

            return connection
        except Exception as e:
            return Response({"Error" : e})
        
    def post(self, request, username):
        try:
            serializer = conectionSerilaizer(data = request.data, context = {'post' : username, 'current_user' : request.user})
            if(serializer.is_valid(raise_exception=True)):
                print(serializer.validated_data)
                serializer.save()
                return Response({"Message": serializer.data}, HTTP_200_OK)
                
            return Response({"Message" : "The post does not exist"}, HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"Error" : e})