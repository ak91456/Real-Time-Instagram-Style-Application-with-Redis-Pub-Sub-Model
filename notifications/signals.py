from django.db.models.signals import post_save
from django.dispatch import receiver
from posts.models import Post, Like, Comment
from .models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from accounts.models import Follow
@receiver(post_save, sender=Post)
def post_created_notify_followers(sender, instance, created, **kwargs):
    if not created:
        return
    post = instance
    actor = post.owner
    followers = actor.followers_set.all().select_related('follower')
    channel_layer = get_channel_layer()
    for f in followers:
        recipient = f.follower
        n = Notification.objects.create(
            recipient=recipient,
            actor=actor,
            verb='posted',
            target_post_id=post.id
        )
        payload = {
            'id': n.id,
            'actor': actor.username,
            'verb': n.verb,
            'post_id': n.target_post_id,
            'created_at': n.created_at.isoformat(),
        }
        group_name = f'notifications_user_{recipient.id}'
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'notification.message',
                'payload': payload,
            }
        )
@receiver(post_save, sender=Like)
def like_notify_owner(sender, instance, created, **kwargs):
    if not created:
        return
    like = instance
    post = like.post
    actor = like.user
    if post.owner == actor:
        return
    n = Notification.objects.create(recipient=post.owner, actor=actor, verb='liked', target_post_id=post.id)
    payload = {'id': n.id, 'actor': actor.username, 'verb': n.verb, 'post_id': n.target_post_id, 'created_at': n.created_at.isoformat()}
    channel_layer = get_channel_layer()
    group_name = f'notifications_user_{post.owner.id}'
    async_to_sync(channel_layer.group_send)(group_name, {'type':'notification.message','payload':payload})
@receiver(post_save, sender=Comment)
def comment_notify_owner(sender, instance, created, **kwargs):
    if not created:
        return
    comment = instance
    post = comment.post
    actor = comment.user
    if post.owner == actor:
        return
    n = Notification.objects.create(recipient=post.owner, actor=actor, verb='commented', target_post_id=post.id)
    payload = {'id': n.id, 'actor': actor.username, 'verb': n.verb, 'post_id': n.target_post_id, 'created_at': n.created_at.isoformat()}
    channel_layer = get_channel_layer()
    group_name = f'notifications_user_{post.owner.id}'
    async_to_sync(channel_layer.group_send)(group_name, {'type':'notification.message','payload':payload})
