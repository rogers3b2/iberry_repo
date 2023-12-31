# Generated by Django 4.2.2 on 2023-09-22 01:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0023_remove_complain_service_alter_complain_complain'),
    ]

    operations = [
        migrations.RenameField(
            model_name='complain',
            old_name='complain_id',
            new_name='complain_placed_id',
        ),
        migrations.CreateModel(
            name='ComplainType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='complain',
            name='complain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.complaintype'),
        ),
    ]
