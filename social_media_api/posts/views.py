from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status, generics  # Add generics here
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification

# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions are only allowed to the author
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'content']
    filterset_fields = ['author']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'author']
    
    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        # Create notification for post author if it's not the comment author
        if comment.post.author != self.request.user:
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb="commented on your post",
                content_type=ContentType.objects.get_for_model(comment.post),
                object_id=comment.post.id
            )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feed(request):
    """
    Return posts from users that the current user follows,
    ordered by creation date (newest first)
    """
    # Get users that the current user follows
    following_users = request.user.following.all()
    
    # Get posts from these users
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    
    # Apply pagination
    paginator = StandardResultsSetPagination()
    result_page = paginator.paginate_queryset(posts, request)
    
    # Serialize the data
    serializer = PostSerializer(result_page, many=True, context={'request': request})
    
    # Return paginated response
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    """Like a post"""
    # Use generics.get_object_or_404 instead of get_object_or_404
    post = generics.get_object_or_404(Post, pk=pk)
    
    # Check if user already liked this post
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        return Response(
            {"error": "You have already liked this post."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create notification for post author if it's not the same user
    if post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            content_type=ContentType.objects.get_for_model(post),
            object_id=post.id
        )
    
    return Response(
        {"success": f"You liked the post '{post.title}'"},
        status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    """Unlike a post"""
    # Update this line to use generics.get_object_or_404
    post = generics.get_object_or_404(Post, pk=pk)
    
    # Try to find and delete the like
    try:
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
        return Response(
            {"success": f"You unliked the post '{post.title}'"},
            status=status.HTTP_200_OK
        )
    except Like.DoesNotExist:
        return Response(
            {"error": "You have not liked this post."},
            status=status.HTTP_400_BAD_REQUEST
        )
