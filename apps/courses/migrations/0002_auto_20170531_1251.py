# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-05-31 12:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ideo',
            new_name='video',
        ),
    ]