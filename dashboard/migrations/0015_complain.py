# Generated by Django 4.2.2 on 2023-08-26 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_service_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complain', models.CharField(choices=[(0, 'Not Working'), (1, 'Have Some issue'), (2, 'Other')], max_length=100)),
                ('description', models.TextField()),
                ('note', models.TextField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.room')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.service')),
            ],
        ),
    ]
