# Generated by Django 3.2.6 on 2021-08-06 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210806_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promo',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='promo', to='main.category', verbose_name='Категория товара'),
        ),
    ]
