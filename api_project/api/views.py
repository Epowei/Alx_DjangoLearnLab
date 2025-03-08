from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets, permissions
from .models import Book
from .serializers import BookSerializer

# Create your views here.
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# Add new ViewSet
class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing book instances.
    Permissions:
    - List/Retrieve: Authenticated users only
    - Create/Update/Delete: Admin users only
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Custom permission logic:
        - GET requests: require authentication
        - Other requests: require admin status
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]