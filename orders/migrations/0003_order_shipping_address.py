# Generated by Django 3.1.2 on 2020-11-13 01:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_auto_20201113_0559'),
        ('orders', '0002_auto_20201106_0239'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.shippingaddress'),
        ),
    ]
