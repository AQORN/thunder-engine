# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nodespec',
            old_name='nodespec',
            new_name='nodelist',
        ),
    ]
