from django.db import models
from django.utils import tree
from mybooksite.models import Book
from django.contrib.auth.models import User


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, blank=True)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)


    def __str__(self):

        return self.user.username




    
