from django.db import models

class UploadedFile(models.Model):
    FILE_TYPES = (
        ('image', 'Image'),
        ('pdf', 'PDF'),
    )

    file = models.FileField(upload_to='uploads/')
    file_name = models.CharField(max_length=10,null=True)
    file_type = models.CharField(choices=FILE_TYPES, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name