from email.policy import default
from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):

    gender_choice = (
        ("Male","Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(upload_to="avatar", default="default.jpg")
    address = models.CharField(max_length=100, null=True, blank=True)
    cellphone_number = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=gender_choice, default="Other")


    def __str__(self):
        return self.user.username



