# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-06-18 15:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20170617_2255'),
        ('courses', '0003_auto_20170604_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_org',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrg', verbose_name='\u6240\u5c5e\u8bfe\u7a0b\u673a\u6784'),
        ),
    ]
