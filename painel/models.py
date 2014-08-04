from django.db import models
from django.contrib.auth.models import User

class History(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField(auto_now_add=True, blank=True)
    panels = models.TextField()
    genes = models.TextField()
    filename = models.TextField()
