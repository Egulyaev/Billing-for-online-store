# Generated by Django 3.2.6 on 2021-09-18 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_promo_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchases',
            name='buy_date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Дата покупки'),
        ),
    ]
