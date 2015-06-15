# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0002_auto_20150128_0724'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nodelist',
            name='node_typeid',
        ),
    ]
