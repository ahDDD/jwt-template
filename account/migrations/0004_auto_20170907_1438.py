# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-07 06:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20170906_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='doctor_image'),
        ),
        migrations.AlterField(
            model_name='doctorprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
