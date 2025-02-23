from django.shortcuts import render, redirect, get_list_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from .models import UserProfile
from .models import Library
from .models import Book
from .forms import BookForm

# Create your views here.

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Function-based view for user registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('list_books')  # Redirect to book list after success
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Class-based view for login (using Django's built-in LoginView)
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True  # Redirect if already logged in
    next_page = 'list_books'  # Redirect to book list after login

# Class-based view for logout (using Django's built-in LogoutView)
class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'

# Role check functions
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Role-based views
@user_passes_test(is_admin, login_url='login')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html', {'message': 'Welcome, Admin!'})

@user_passes_test(is_librarian, login_url='login')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html', {'message': 'Welcome, Librarian!'})

@user_passes_test(is_member, login_url='login')
def member_view(request):
    return render(request, 'relationship_app/member_view.html', {'message': 'Welcome, Member!'})


# New permission-based views
@permission_required('relationship_app.can_add_book', login_url='login')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})

@permission_required('relationship_app.can_change_book', login_url='login')
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})

@permission_required('relationship_app.can_delete_book', login_url='login')
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})