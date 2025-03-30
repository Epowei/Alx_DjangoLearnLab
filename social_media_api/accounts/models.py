from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    followers = models.ManyToManyField(
        'self', 
        symmetrical=False,
        related_name='following',
        blank=True
    )

    def __str__(self):
        return self.username
    
    def follow(self, user):
        """Follow another user if not already following"""
        if user != self and user not in self.following.all():
            user.followers.add(self)
            return True
        return False
    
    def unfollow(self, user):
        """Unfollow a currently followed user"""
        if user in self.following.all():
            user.followers.remove(self)
            return True
        return False
    
    @property
    def following_count(self):
        return self.following.count()
    
    @property
    def followers_count(self):
        return self.followers.count()
