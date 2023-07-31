from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    # avatar = models.ImageField(height_field=60, width_field=60, blank=True, null=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.pk])


class Comment(models.Model):
    PRODUCT_STARS = [
        ('1', 'Very Bad',),
        ('2', 'Bad',),
        ('3', 'Normal',),
        ('4', 'Good',),
        ('5', 'Perfect',),
    ]

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=3000)
    stars = models.CharField(max_length=10, choices=PRODUCT_STARS)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    # buyer = models.BooleanField(default=True) -> This should be in CustomUser and a FK to here
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.product.id])
