from django.contrib.auth.models import User
from django.db import models


class File(models.Model):
    file = models.FileField(null=False, blank=False, upload_to='uploads')
    name = models.CharField(max_length=100, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.file
