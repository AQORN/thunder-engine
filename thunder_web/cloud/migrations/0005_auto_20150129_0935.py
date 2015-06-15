# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0004_auto_20150129_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noderole',
            name='node',
            field=models.ForeignKey(related_name='roles', to='cloud.Nodelist'),
            preserve_default=True,
        ),
    ]
