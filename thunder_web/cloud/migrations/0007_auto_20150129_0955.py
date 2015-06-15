# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0006_auto_20150129_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noderole',
            name='role',
            field=models.ForeignKey(related_name='nodeRoles', to='cloud.Roletype', null=True),
            preserve_default=True,
        ),
    ]
