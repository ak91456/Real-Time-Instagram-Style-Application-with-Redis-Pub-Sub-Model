from rest_framework import serializers
from .models import User, Follow
from django.contrib.auth.password_validation import validate_password
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('username','email','password','password2')
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password':'Passwords must match.'})
        return attrs
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers_set.count', read_only=True)
    following_count = serializers.IntegerField(source='following_set.count', read_only=True)
    class Meta:
        model = User
        fields = ('id','username','email','bio','avatar','followers_count','following_count')
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('id','follower','following','created_at')
        read_only_fields = ('created_at',)
