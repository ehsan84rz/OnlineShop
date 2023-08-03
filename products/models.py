from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'))
    price = models.PositiveIntegerField(default=0, verbose_name=_('price'))
    active = models.BooleanField(default=True)
    # avatar = models.ImageField(height_field=60, width_field=60, blank=True, null=True)
    image = models.ImageField(verbose_name=_('Product Image'), upload_to='product/product_cover/', blank=True)

    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('datetime_created'))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_('datetime_modified'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.pk])


class ActiveCommentsManager(models.Manager):
    def get_queryset(self):
        return super(ActiveCommentsManager, self).get_queryset().filter(active=True)


class Comment(models.Model):
    PRODUCT_STARS = [
        ('1', _('Very Bad'),),
        ('2', _('Bad'),),
        ('3', _('Normal'),),
        ('4', _('Good'),),
        ('5', _('Perfect'),),
    ]

    author = models.ForeignKey(get_user_model(),
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name=_('author'))
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=3000, verbose_name=_('comment text'))
    stars = models.CharField(max_length=10, choices=PRODUCT_STARS, verbose_name=_('What is your score?'))

    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('datetime_created'))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_('datetime_modified'))

    # buyer = models.BooleanField(default=True) -> This should be in CustomUser and a FK to here
    active = models.BooleanField(default=True, verbose_name=_('active'))

    # Manager (--method 3--)
    objects = models.Manager()
    active_comments_manager = ActiveCommentsManager

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.product.id])
