from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
import os

# Create your models here.
class Document(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')
    file_type = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + "." + self.file_type

@receiver(models.signals.post_delete, sender=Document)
def delete_file(sender, instance, **kwargs):
    '''After Document is deleted from database, a signal is sent to delete the associated file in the server'''
    if instance.file:
        if os.path.isfile(instance.file.path):  # Ensure file exists before deleting
            os.remove(instance.file.path)    
