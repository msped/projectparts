# Generated by Django 3.2.7 on 2021-10-03 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.ImageField(default='default.jpg', upload_to=''),
        ),
    ]
