# Generated by Django 4.2.2 on 2023-08-27 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0020_alter_complain_options_complain_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='complain',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Complained'), (1, 'Processing'), (2, 'Completed'), (3, 'Canceled')], default=0),
        ),
    ]
