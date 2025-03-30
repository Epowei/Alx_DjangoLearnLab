from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    # User who receives the notification
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    # User who triggered the notification
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='actions'
    )
    # Description of the action
    verb = models.CharField(max_length=255)
    # Flag for read/unread
    unread = models.BooleanField(default=True)
    # When it was created
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Generic relation to any object (post, comment, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.actor} {self.verb} -> {self.recipient}"
