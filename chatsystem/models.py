from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


