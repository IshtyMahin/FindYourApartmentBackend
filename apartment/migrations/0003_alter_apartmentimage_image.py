# Generated by Django 5.0.1 on 2024-05-21 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0002_alter_apartmentimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartmentimage',
            name='image',
            field=models.ImageField(blank=True, default='', null=True, upload_to='apartment_images/'),
        ),
    ]
