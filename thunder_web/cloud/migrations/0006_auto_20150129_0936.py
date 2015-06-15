# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0005_auto_20150129_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noderole',
            name='node',
            field=models.ForeignKey(related_name='nodes', to='cloud.Nodelist'),
            preserve_default=True,
        ),
    ]
