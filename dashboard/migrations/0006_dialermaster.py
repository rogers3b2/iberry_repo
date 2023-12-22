# Generated by Django 4.2.2 on 2023-06-10 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_room_auth_token_alter_room_room_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='DialerMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c2c_name', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]