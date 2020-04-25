from django.db import models


# TODO:rename to biometric + finger(processed)
class Image(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField('date added')
    image = models.ImageField(upload_to='image')


class ProcessedImage(models.Model):
    name = models.CharField(max_length=110)
    url = models.CharField(max_length=256)
