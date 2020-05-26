from django.db import models


class Biometric(models.Model):
    id = models.CharField(primary_key=True, serialize=False, verbose_name='ID', max_length=36)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField('creation date')
    image_name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=256)
    lower_thresh = models.IntegerField()
    upper_thresh = models.IntegerField()
    denoise_lvl = models.IntegerField()
    clahe_lvl = models.IntegerField()
    gauss_block_size = models.IntegerField()
    gauss_constant = models.IntegerField()
    preprocessed_url = models.CharField(max_length=256)
    gauss_url = models.CharField(max_length=256)
    grabcut_url = models.CharField(max_length=256)
    grabcut_gauss_url = models.CharField(max_length=256)


class LoadedImage(models.Model):
    id = models.CharField(primary_key=True, serialize=False, verbose_name='ID', max_length=36)
    created_at = models.DateTimeField('date added')
    image = models.ImageField(upload_to='image')
