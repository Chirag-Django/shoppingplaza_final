# Generated by Django 3.1.2 on 2020-10-30 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0005_product_product_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]