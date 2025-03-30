from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, LoginSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import CustomUser

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# New view to list all users
class UserListView(generics.ListAPIView):
    """List all users in the system"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Add the request to context so UserSerializer can check if user is following
        context['request'] = self.request
        return context

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    """API endpoint for following a user"""
    user_to_follow = get_object_or_404(CustomUser, id=user_id)
    
    if request.user == user_to_follow:
        return Response(
            {"error": "You cannot follow yourself."}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if request.user.follow(user_to_follow):
        return Response(
            {"success": f"You are now following {user_to_follow.username}"},
            status=status.HTTP_200_OK
        )
    
    return Response(
        {"error": f"You are already following {user_to_follow.username}"},
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    """API endpoint for unfollowing a user"""
    user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
    
    if request.user.unfollow(user_to_unfollow):
        return Response(
            {"success": f"You have unfollowed {user_to_unfollow.username}"},
            status=status.HTTP_200_OK
        )
    
    return Response(
        {"error": f"You are not following {user_to_unfollow.username}"},
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_followers(request):
    """Get list of users following the current user"""
    followers = request.user.followers.all()
    serializer = UserSerializer(
        followers, 
        many=True,
        context={'request': request}
    )
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_following(request):
    """Get list of users the current user is following"""
    following = request.user.following.all()
    serializer = UserSerializer(
        following, 
        many=True,
        context={'request': request}
    )
    return Response(serializer.data)