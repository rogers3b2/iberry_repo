# Generated by Django 4.2.2 on 2023-07-04 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_alter_notification_notification_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.SmallIntegerField(choices=[(0, 'Order Placed'), (1, 'Report'), (2, 'Public')], default=0),
        ),
    ]
