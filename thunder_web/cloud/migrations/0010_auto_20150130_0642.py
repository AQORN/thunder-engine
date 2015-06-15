# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0009_auto_20150129_1109'),
    ]

    operations = [
        migrations.RenameField(
            model_name='noderole',
            old_name='nodereole_details',
            new_name='noderole_details',
        ),
    ]
