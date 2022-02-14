from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.text import slugify


class Book(models.Model):
    rating_choice = (
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
    )
   
    title = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    rating = models.PositiveIntegerField(choices=rating_choice)
    description = models.TextField()
    img = models.ImageField(upload_to="book_img", null=True, blank=True)
    thumbnail = models.ImageField(upload_to="book_thumbnails", null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def is_in_stock(self):
        if self.quantity > 0:
            return 'in stock'
        return 'out of stock'
        
        

    def __str__(self):
        return self.title

    


class Category(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, blank=True, related_name="categories")
    
    def __str__(self):
        return self.name






