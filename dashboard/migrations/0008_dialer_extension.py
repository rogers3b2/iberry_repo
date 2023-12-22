# Generated by Django 4.2.2 on 2023-06-10 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_rename_dialermaster_dialer'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialer',
            name='extension',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dashboard.extension'),
            preserve_default=False,
        ),
    ]
