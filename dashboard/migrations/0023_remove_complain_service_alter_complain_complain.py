# Generated by Django 4.2.2 on 2023-09-11 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0022_alter_complain_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complain',
            name='service',
        ),
        migrations.AlterField(
            model_name='complain',
            name='complain',
            field=models.CharField(max_length=150),
        ),
    ]