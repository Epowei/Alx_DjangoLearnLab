from django.db import models

# Author model represents an author who can have multiple books
class Author(models.Model):
    name = models.CharField(max_length=100, help_text="The author's full name")
    
    def __str__(self):
        return self.name

# Book model represents a book written by an author
class Book(models.Model):
    title = models.CharField(max_length=200, help_text="The title of the book")
    publication_year = models.IntegerField(help_text="The year the book was published")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        help_text="The author who wrote this book"
    )
    
    def __str__(self):
        return self.title