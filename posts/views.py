from rest_framework import viewsets, permissions, status, generics
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.models import Follow
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at').select_related('owner').prefetch_related('likes','comments')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        obj, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            obj.delete()
            return Response({'liked': False})
        return Response({'liked': True})
    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def comment(self, request, pk=None):
        post = self.get_object()
        text = request.data.get('text', '').strip()
        if not text:
            return Response({'detail':'text is required'}, status=status.HTTP_400_BAD_REQUEST)
        Comment.objects.create(user=request.user, post=post, text=text)
        return Response({'commented': True})
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        following_ids = list(user.following_set.values_list('following_id', flat=True)) + [user.id]
        return Post.objects.filter(owner_id__in=following_ids).order_by('-created_at').select_related('owner').prefetch_related('likes','comments')
