# Generated by Django 4.2.2 on 2023-08-05 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0016_remove_item_category_remove_item_sub_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_type',
            field=models.CharField(choices=[('None', 'None'), ('Veg', 'Veg'), ('Non Veg', 'Non Veg')], default=0, max_length=20),
        ),
    ]