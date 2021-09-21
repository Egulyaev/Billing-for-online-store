from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Наименование категории'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Поле формирования Slug для категории'
    )
    description = models.TextField(verbose_name='Описание категории')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'


class Product(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Наименование товара'
    )
    description = models.TextField(verbose_name='Описание продукта')
    price = models.IntegerField(verbose_name='Цена')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='product',
        verbose_name='Группа поста'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'


class Purchases(models.Model):
    buy_time = models.DateTimeField(
        blank=False,
        null=True,
        auto_now_add=True,
        verbose_name='Время покупки'
    )
    buy_date = models.DateField(
        blank=False,
        null=True,
        auto_now_add=True,
        verbose_name='Дата покупки'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        related_name='purchases',
        verbose_name='Покупки'
    )
    buyer = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='purchases',
        verbose_name='Покупатель'
    )
    promo_price = models.IntegerField(
        null=True,
        verbose_name='Цена с учетом скидки'
    )

    class Meta:
        verbose_name_plural = 'Покупки'
        verbose_name = 'Покупка'


class Promo(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование акции'
    )
    percent = models.IntegerField(
        verbose_name='Размер скидки'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='promo',
        verbose_name='Категория товара'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name='promo',
        verbose_name='Покупки'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Акции'
        verbose_name = 'Акция'
