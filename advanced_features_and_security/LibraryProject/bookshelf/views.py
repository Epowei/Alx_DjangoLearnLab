from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.html import escape
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.http import Http404

from .models import Book
from .forms import BookForm

@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
@require_GET  # Only allow GET requests for this view
def book_detail(request, pk):
    try:
        # Validate that pk is an integer
        pk = int(pk)
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'bookshelf/book_detail.html', {'book': book})
    except ValueError:
        # Handle case where pk is not an integer
        raise Http404("Book not found")

@login_required
@require_GET
def book_list(request):
    # Everyone can see the list, but we'll filter what they can see
    if request.user.has_perm('bookshelf.can_view_book'):
        # Use proper queryset filtering and limit results
        books = Book.objects.all()[:100]  # Limit to first 100 books to prevent DoS
    else:
        books = []
        messages.warning(request, "You don't have permission to view books.")
    
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
@require_http_methods(["GET", "POST"])  # Only allow GET and POST requests
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            try:
                # Use a transaction to ensure database integrity
                with transaction.atomic():
                    # Clean data before saving
                    new_book = form.save(commit=False)
                    # Additional validation if needed
                    new_book.full_clean()
                    new_book.save()
                
                messages.success(request, "Book created successfully!")
                return redirect('book_list')
            except ValidationError as e:
                # Add form errors from the validation
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Create'})

@login_required
@permission_required('bookshelf.can_edit_book', raise_exception=True)
@require_http_methods(["GET", "POST"])
def book_edit(request, pk):
    try:
        # Validate pk is an integer
        pk = int(pk)
        book = get_object_or_404(Book, pk=pk)
        
        if request.method == 'POST':
            form = BookForm(request.POST, instance=book)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        updated_book = form.save(commit=False)
                        updated_book.full_clean()
                        updated_book.save()
                    
                    messages.success(request, "Book updated successfully!")
                    return redirect('book_list')
                except ValidationError as e:
                    for field, errors in e.message_dict.items():
                        for error in errors:
                            form.add_error(field, error)
        else:
            form = BookForm(instance=book)
        
        return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Edit'})
    except ValueError:
        raise Http404("Book not found")

@login_required
@permission_required('bookshelf.can_delete_book', raise_exception=True)
@require_http_methods(["GET", "POST"])
def book_delete(request, pk):
    try:
        # Validate pk is an integer
        pk = int(pk)
        book = get_object_or_404(Book, pk=pk)
        
        if request.method == 'POST':
            # Use transaction for consistency
            with transaction.atomic():
                book_title = book.title  # Store before deletion for message
                book.delete()
            
            messages.success(request, f"Book '{escape(book_title)}' deleted successfully!")
            return redirect('book_list')
        
        return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})
    except ValueError:
        raise Http404("Book not found")