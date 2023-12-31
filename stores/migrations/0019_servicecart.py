# Generated by Django 4.2.2 on 2023-09-10 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0022_alter_complain_status'),
        ('stores', '0018_remove_item_category_item_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.room')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.service')),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('room', 'service')},
            },
        ),
    ]
