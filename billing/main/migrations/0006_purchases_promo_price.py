# Generated by Django 3.2.6 on 2021-09-20 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_purchases_buy_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchases',
            name='promo_price',
            field=models.IntegerField(null=True, verbose_name='Цена с учетом скидки'),
        ),
    ]
