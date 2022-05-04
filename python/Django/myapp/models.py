from django.db import models

# Create your models here.
# ORM - Object Relational Mapping

class User(models.Model):

    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=20)
    pic = models.FileField(upload_to='Profile',default='avtar.png')

    def __str__(self):
        return self.email