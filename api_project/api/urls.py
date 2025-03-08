from django.urls import path, include
from .views import BookList, BookViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

# Create router instance
router = DefaultRouter()
# Register the ViewSet with basename since we don't have a queryset-defined URL name
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),  # Maps to the BookList view
    # Include all router-generated URLs
    path('', include(router.urls)),
    path('token-auth/', obtain_auth_token, name='api_token_auth'),  # Add this URL pattern for the token
]
