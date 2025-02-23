# Update Command

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