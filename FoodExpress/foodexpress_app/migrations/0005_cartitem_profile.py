# Generated by Django 5.0 on 2023-12-27 16:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodexpress_app', '0004_alter_category_managers_remove_profile_avatar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='profile',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='foodexpress_app.profile'),
        ),
    ]
