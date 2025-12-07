from rest_framework import generics, permissions, status
from .serializers import RegisterSerializer, UserSerializer
from .models import User, Follow
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_toggle(request, pk):
    me = request.user
    try:
        target = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'detail':'User not found'}, status=404)
    if me == target:
        return Response({'detail':'Cannot follow yourself'}, status=400)
    obj, created = Follow.objects.get_or_create(follower=me, following=target)
    if not created:
        obj.delete()
        return Response({'followed': False})
    return Response({'followed': True})
