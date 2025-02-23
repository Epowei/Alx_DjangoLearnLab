# relationship_app/urls.py
from django.urls import path
from .views import list_books, LibraryDetailView

app_name = 'relationship_app'

urlpatterns = [
    path('books/', list_books, name='list_books'),  # Function-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # Class-based view
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),  # Built-in LoginView
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),  # Built-in LogoutView
    path('register/', views.register, name='register'),
]