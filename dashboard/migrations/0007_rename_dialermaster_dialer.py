# Generated by Django 4.2.2 on 2023-06-10 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_dialermaster'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DialerMaster',
            new_name='Dialer',
        ),
    ]
