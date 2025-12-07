from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    bio = models.TextField(blank=True, default='')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    def __str__(self):
        return self.username
class Follow(models.Model):
    follower = models.ForeignKey('accounts.User', related_name='following_set', on_delete=models.CASCADE)
    following = models.ForeignKey('accounts.User', related_name='followers_set', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('follower','following')
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.follower} -> {self.following}"
