from django.db import models
import os

class Categories(models.Model):
    name = models.CharField(max_length=255, unique=True)
    img_category = models.ImageField(upload_to='categories', null=True)
    def __str__(self):
        return self.name

from django.core.validators import FileExtensionValidator

class Upload(models.Model):
    file_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='pdfs/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, related_name='uploads', null=True)

    def __str__(self):
        return f'Archivo: {self.file_name}, categoria: {self.category}'

    @property
    def filename(self):
        return os.path.basename(self.pdf_path.name).split('.')[0]

class User(models.Model):
    name = models.CharField(max_length=255, unique=True, default=None)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    linkedin = models.CharField(max_length=255, blank=True, null=True)
    orcid = models.CharField(max_length=255, unique=True, blank=True, null=True)
    visible = models.BooleanField(default=True)
    img_profile_path = models.ImageField(upload_to='profile', null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'Usuario: {self.name} ({self.username})'



