# Generated by Django 2.2.5 on 2019-11-08 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('is_paid', models.BooleanField(default=False)),
                ('order_date', models.DateField(null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.Product')),
            ],
        ),
    ]