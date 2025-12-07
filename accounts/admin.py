from django.contrib import admin
from .models import User, Follow
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass
@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower','following','created_at')
