# Generated by Django 5.0.6 on 2024-05-25 18:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_item_discount_price_item_is_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
