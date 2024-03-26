from django.db import models
from django.contrib.auth.models import User
    
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.title
