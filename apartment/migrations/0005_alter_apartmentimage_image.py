# Generated by Django 5.0.1 on 2024-06-06 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0004_booking_favoriteapartment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartmentimage',
            name='image',
            field=models.URLField(blank=True, default='', null=True),
        ),
    ]
