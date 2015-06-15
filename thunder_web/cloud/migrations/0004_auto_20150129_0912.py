# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0003_remove_nodelist_node_typeid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noderole',
            name='node',
            field=models.ForeignKey(related_name='nodes', to='cloud.Nodelist'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='noderole',
            name='role',
            field=models.ForeignKey(related_name='roles', to='cloud.Roletype'),
            preserve_default=True,
        ),
    ]
