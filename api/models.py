from django.db import models

# Create your models here.
from django.db import models


class Conversation(models.Model):

    topic = models.CharField(max_length=255)

    question = models.TextField()

    answer = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic
