# Create

## Command input
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
```
## Output
```python
>>> book
<Book: 1984>
```

# Retrieve

## Command input
```python
>>> book = Book.objects.get(title="1984")
>>> print(f"Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")
```
## Output
```python
>>> Title: 1984, Author: George Orwell, Year: 1949
```

# Update

## Command input
```python
>>> book = Book.objects.get(title="1984")
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()
```
## Output
```python
>>> book
<Book: Nineteen Eighty-Four>
```

# Delete

## Command input and output
```python
>>> book = Book.objects.get(title="Nineteen Eighty-Four")
>>> book.delete()
(1, {'bookshelf.Book': 1})
>>> Book.objects.all()
<QuerySet []>
```