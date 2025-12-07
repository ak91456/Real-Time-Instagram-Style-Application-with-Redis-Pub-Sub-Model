from rest_framework import serializers
from .models import Post, Like, Comment
from accounts.serializers import UserSerializer
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id','user','text','created_at')
class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Like
        fields = ('id','user','created_at')
class PostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ('id','owner','image','caption','created_at','likes_count','comments')
