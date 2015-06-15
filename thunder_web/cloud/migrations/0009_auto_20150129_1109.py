# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0008_roletype_role_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roletype',
            name='role_details',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
