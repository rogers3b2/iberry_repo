# Generated by Django 4.2.2 on 2023-07-27 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0012_orderitem_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.IntegerField(editable=False),
        ),
    ]