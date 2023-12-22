# Generated by Django 4.2.2 on 2023-09-11 00:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0022_alter_complain_status'),
        ('stores', '0020_remove_servicecart_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=8, unique=True)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.SmallIntegerField(choices=[(0, 'Ordered'), (1, 'Processing'), (2, 'Completed'), (3, 'Canceled')], default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.room')),
                ('services', models.ManyToManyField(related_name='stores_order_services', to='dashboard.service')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]