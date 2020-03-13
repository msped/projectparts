# Generated by Django 3.0.2 on 2020-03-12 23:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('checkout', '0001_initial'),
        ('cart', '0002_auto_20200312_2350'),
        ('competition', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='entries',
            name='competition_entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='competition.Competition'),
        ),
        migrations.AddField(
            model_name='entries',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cart.Order'),
        ),
        migrations.AddField(
            model_name='entries',
            name='orderItem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cart.OrderItem'),
        ),
        migrations.AddField(
            model_name='entries',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]