from django.contrib import admin
from .models import Post, Like, Comment
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id','owner','created_at')
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user','post','created_at')
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','post','created_at')
