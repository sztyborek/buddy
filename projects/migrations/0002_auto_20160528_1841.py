# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(default='', unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(unique=True, max_length=255, verbose_name='Name of the project'),
        ),
        migrations.AlterField(
            model_name='project',
            name='number_of_users_required',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
