# Generated by Django 5.0.1 on 2024-06-06 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0005_alter_apartmentimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartmentimage',
            name='image',
            field=models.ImageField(blank=True, default='', null=True, upload_to='apartment_images/'),
        ),
    ]
