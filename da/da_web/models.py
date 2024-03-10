from django.db import models


class ConversationLog(models.Model):
    speaker = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)