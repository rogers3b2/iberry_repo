# Generated by Django 4.2.2 on 2023-07-04 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[(0, 'Order Placed'), (1, 'Report'), (2, 'Public')], default=0, max_length=25),
        ),
    ]
