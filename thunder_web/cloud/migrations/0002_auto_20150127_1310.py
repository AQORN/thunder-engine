# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nodelist',
            name='cloud',
        ),
        migrations.AddField(
            model_name='nodelist',
            name='cloud_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
