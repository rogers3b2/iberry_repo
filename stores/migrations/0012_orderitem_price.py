# Generated by Django 4.2.2 on 2023-07-27 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0011_price_sell_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]
