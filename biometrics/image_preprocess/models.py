from django.db import models


# TODO:rename to biometric + finger(processed)
class Image(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField('date added')
    image = models.ImageField(upload_to='image')
    processed_url = models.CharField(max_length=256)
    lower_thresh = models.IntegerField()
    upper_thresh = models.IntegerField()
