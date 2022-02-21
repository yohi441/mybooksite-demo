from email.policy import default
from django.db import models
from django.contrib.auth.models import User



gender_choice = (
        ("Male","Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )

class Profile(models.Model):

    
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(upload_to="avatar/", null=True, blank=True)
    address = models.CharField(max_length=100, null=True)
    cellphone_number = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=6, choices=gender_choice, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username



