from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="images", blank=True, null=True)
    lighting = models.CharField(max_length=20)

    @property
    def is_current_user(self):
        # allows client to read this value = getter 

        return self.__is_current_user

    @is_current_user.setter
    def is_current_user(self, value):
        # allows client to set this value = setter
        self.__is_current_user = value