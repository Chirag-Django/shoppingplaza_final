# Generated by Django 3.1.2 on 2020-10-30 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0004_product_featured_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_active',
            field=models.BooleanField(default=True),
        ),
    ]
