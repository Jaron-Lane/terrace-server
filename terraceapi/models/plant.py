from django.db import models
from django.contrib.auth.models import User

class Plant(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    nick_name = models.CharField(max_length=50)
    location = models.ForeignKey("Location", on_delete=models.CASCADE)
    bio = models.CharField(max_length=500)
    # photo = models.ImageField(_(""), upload_to=None, height_field=None, width_field=None, max_length=None)
    watering_frequency = models.IntegerField()
    date_watered = models.DateField(_(""), auto_now=False, auto_now_add=False)