from django.contrib.auth.models import User
from django.db import models

FILE_STATUS = (
    ('common', 'common'),
    ('hidden', 'hidden'),
    ('private', 'private')
)

class File(models.Model):
    file = models.FileField(null=False, blank=False, upload_to='uploads')
    name = models.CharField(max_length=100, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    file_status = models.CharField(max_length=20, verbose_name='Статус проекта', choices=FILE_STATUS,
                                      default=FILE_STATUS[0][0])

    def __str__(self):
        return self.name


class Private(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)