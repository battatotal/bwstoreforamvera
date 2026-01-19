from django.db import models
from django.urls import reverse


class Category(models.Model):

    name = models.CharField(max_length=200, db_index=True, verbose_name="Имя")
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):

    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE, verbose_name="Категории товаров")
    name = models.CharField(max_length=200, db_index=True, verbose_name="Название товара")
    slug = models.SlugField(max_length=200, db_index=True)
    imageMain = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name="Основное изображение")
    image1 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name="Изображение 1")
    image2 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name="Изображение 2")
    image3 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name="Изображение 3")
    image4 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name="Изображение 4")
    description = models.TextField(blank=True, verbose_name="Описание")
    materials = models.TextField(blank=True, verbose_name="Материалы")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    size = models.CharField(max_length=200, verbose_name="Размер")
    available = models.BooleanField(default=True, verbose_name="Доступен")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Добавлен")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    quantity = models.IntegerField(verbose_name="Количество в наличии")

    class Meta:

        ordering = ('name',)
        # index_together = (('id', 'slug'),)     < Устарело (depricated)
        indexes = [models.Index(fields=["id", "slug"])]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
