from django.db import models
from .slug import unique_slugify
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self, **kwargs):
        slug = '%s' % (self.name)
        unique_slugify(self, slug)
        super(Category, self).save()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:item_list_by_category',
        args=[self.slug])


class Item(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    ingredients = models.TextField(max_length=400)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='items/',
                            blank=True)
    available = models.BooleanField(default=True)

    class Meta: 
        ordering = ('name',)
        verbose_name = 'item'
        verbose_name_plural = 'items'

    def __str__(self):
        return self.name
