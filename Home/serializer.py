from rest_framework import serializers
from .models import *
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

class userregisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        extra_kwargs = (
            {
                'username': {'required' : True}
            }
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)   
        return user
        
class userloginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

        extra_kwargs = (
            {
                'username': {'required' : True}
            }
        )

class userpostSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_comment = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    total_deslikes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    my_comments = serializers.SerializerMethodField()

    do_like = serializers.SerializerMethodField()
    do_comment = serializers.SerializerMethodField()
    all_comments = serializers.SerializerMethodField()
    make_friend = serializers.SerializerMethodField()

    delete_post = serializers.SerializerMethodField()

    class Meta:
        model = Posts
        fields = ['id','user_name', 'images', 'caption', 'is_liked', 'is_comment', 'total_likes', 'total_deslikes', 'total_comments', 'my_comments', 'do_like', 'do_comment', 'all_comments', 'make_friend', 'delete_post']

        extra_kwargs = (
            {
                'is_liked': {'read_only' : True},
                'is_comment': {'read_only' : True},
                'make_friend': {'read_only' : True}
            }
        )

    def get_user_name(self, obj):
        return obj.user.username   

    def get_is_liked(self, obj):
        current_user = self.context['request'].user
        try:
            like_obj = Likes.objects.get(user=current_user, post=obj)
            return like_obj.like
        except Likes.DoesNotExist:
            return False
        
    def get_is_comment(self, obj):
        current_user = self.context['request'].user
        comment_obj = Comments.objects.filter(user=current_user, post=obj).first()

        if(comment_obj):
            return True
        else:
            return False
    
    def get_total_likes(self, obj):
        total_length = Likes.objects.filter(post = obj, like = True).count()
        return total_length
    
    def get_total_deslikes(self, obj):
        total_length = Likes.objects.filter(post = obj, like = False).count()
        return total_length
    
    def get_total_comments(self, obj):
        total_length = Comments.objects.filter(post = obj).count()
        return total_length
    
    def get_my_comments(self, obj):
        current_user = self.context['request'].user

        try:
            comment_obj = Comments.objects.get(user=current_user, post=obj)
            return comment_obj.comment
        except ObjectDoesNotExist:
            return("You haven't commented")

    def get_do_like(self, obj):
        request = self.context.get('request')
        base_url = request.build_absolute_uri('/')
        return f"{base_url}{reverse('likesViewer', kwargs={'pk': obj.id})}"
    
    def get_do_comment(self, obj):
        request = self.context.get('request')
        base_url = request.build_absolute_uri('/')
        return f"{base_url}{reverse('single_commentViewer', kwargs={'pk': obj.id})}"

    def get_all_comments(self, obj):
        request = self.context.get('request')
        base_url = request.build_absolute_uri('/')
        return f"{base_url}{reverse('comments_view', kwargs={'post_id': obj.id})}"

    def get_make_friend(self, obj):
        request = self.context.get('request')
        base_url = request.build_absolute_uri('/')
        return f"{base_url}{reverse('userconnection_View', kwargs={'username' : obj.user.username})}"
    
    def get_delete_post(self, obj):
        reqest = self.context.get('request')
        base_url = reqest.build_absolute_uri('/')

        return f"{base_url}{reverse('deletePost', kwargs={'pk' : obj.id})}"
    
class usercommentsSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    post_caption = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ['id', 'user_name', 'post_caption', 'comment']

    def get_user_name(self, obj):
        return obj.user.username  
      
    def get_user_name(self, obj):
        return obj.post.caption    
    


class likesSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Likes
        fields = ['id', 'user_name', 'post', 'like']

        extra_kwargs = (
            {
                'user': {'read_only' : True},
                'post': {'read_only' : True},
            }
        )

    def get_user_name(self, obj):
        return obj.user.username
    
    def create(self, validated_data):
        user = self.context['user']
        post = self.context['post']

        data = Likes(user = user, post = post)
        data.like = validated_data.get("like")

        data.save()

        return data
        
class commentSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ['id', 'user_name', 'post', 'comment']

        extra_kwargs = (
            {
                'user': {'read_only' : True},
                'post': {'read_only' : True},
            }
        )

    def create(self, validated_data):
        user = self.context['user']
        post = self.context['post']

        data = Comments(comment = validated_data.get('comment'))
        data.user = user
        data.post = post

        data.save()

        return data

    def get_user_name(self, obj):
        return obj.user.username
    

class conectionSerilaizer(serializers.ModelSerializer):
    make_friend = serializers.BooleanField(write_only=True)
    friends = serializers.SerializerMethodField()

    class Meta:
        model = Connection
        fields = ['friends', 'make_friend']

        extra_kwargs = (
            {
                'id' : {'read_only' : True},
                'friends' : {'read_only' : True},
            }
        )

    def get_user(self, obj):
        return obj.user.username
    
    def get_friends(self, obj):
        return [friend.username for friend in obj.friends.all()]


    def validate(self, data):
        current_user = self.context['current_user']
        username = self.context['post']
        
        print(current_user.username)
        print(username)

        if(current_user.username == username):

            raise serializers.ValidationError({"Status" : "Yor can't make friend with your self"})
        
        user = User.objects.filter(username = username).first()
        exitst_friendShip = Connection.objects.filter(user = current_user, friends = user).first()

        if(exitst_friendShip):
            raise serializers.ValidationError({"Mes" : "You are alrady friends"})
        
        return data
    
    def create(self, validated_data):
        current_user = self.context['current_user']
        username = self.context['post']

        user = User.objects.filter(username = username).first()

        obj = Connection.objects.create(user = current_user)
        obj.friends.add(user)
        obj.save()

        return obj