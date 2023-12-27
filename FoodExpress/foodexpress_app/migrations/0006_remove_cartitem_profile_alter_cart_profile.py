# Generated by Django 5.0 on 2023-12-27 18:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodexpress_app', '0005_cartitem_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='profile',
        ),
        migrations.AlterField(
            model_name='cart',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='foodexpress_app.profile'),
        ),
    ]