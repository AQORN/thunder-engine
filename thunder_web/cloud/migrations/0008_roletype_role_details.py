# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0007_auto_20150129_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='roletype',
            name='role_details',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
