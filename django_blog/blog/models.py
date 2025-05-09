from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


# The Tag model is no longer needed as django-taggit provides its own
# You can remove the Tag model code or comment it out
# class Tag(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#     slug = models.SlugField(max_length=50, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.name
    
#     def get_absolute_url(self):
#         """Returns the URL to access a list of posts with this tag."""
#         return reverse('blog:tag-posts', kwargs={'slug': self.slug})


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    # Add the TaggableManager
    tags = TaggableManager(blank=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail view of this post."""
        return reverse('blog:post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']  # Show newest comments first
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
    
    def get_absolute_url(self):
        """Returns the URL to access the post detail page with this comment."""
        return reverse('blog:post-detail', kwargs={'pk': self.post.pk})
