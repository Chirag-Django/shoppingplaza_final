# Generated by Django 3.1.2 on 2020-10-30 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise', '0003_auto_20201030_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='featured_item',
            field=models.BooleanField(default=False),
        ),
    ]
