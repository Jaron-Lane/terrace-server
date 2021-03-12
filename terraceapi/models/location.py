from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    photo = models.ImageField(_(""), upload_to=None, height_field=None, width_field=None, max_length=None)
    lighting = models.CharField(max_length=20)