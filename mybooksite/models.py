from django.db import models
from django.db.models.deletion import CASCADE
from PIL import Image


class Book(models.Model):
    rating_choice = (
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
    )
    availability_choice = (
        ("in_stock", "in_stock"),
        ("out_stack", "out_of_stack")
    )
    
    title = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    rating = models.PositiveIntegerField(choices=rating_choice)
    availability = models.CharField(max_length=10, choices=availability_choice)
    description = models.TextField()
    img = models.ImageField(upload_to="book_img")
    thumbnail = models.ImageField(upload_to="book_thumbnails", null=True, blank=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, blank=True, related_name="categories")
    
    def __str__(self):
        return self.name






