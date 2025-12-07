from django.db import models
from django.conf import settings
class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actions', on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    target_post_id = models.IntegerField(null=True, blank=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
