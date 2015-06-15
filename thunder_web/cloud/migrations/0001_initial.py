# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cloud',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cloud_name', models.CharField(max_length=255)),
                ('created_date', models.DateField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'thunder_cloud',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Nodelist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cloud_id', models.IntegerField(default=0)),
                ('node_ip', models.GenericIPAddressField()),
                ('node_typeid', models.IntegerField()),
                ('host_name', models.CharField(max_length=255)),
                ('user_name', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('sudo_password', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'thunder_nodelist',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Nodelog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('node_listid', models.IntegerField()),
                ('user_ip', models.GenericIPAddressField()),
                ('receipe_id', models.IntegerField()),
                ('log_details', models.TextField()),
                ('user_id', models.IntegerField()),
                ('status', models.BooleanField(default=True)),
                ('log_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'thunder_nodelog',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NodeRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nodereole_details', models.CharField(max_length=255)),
                ('node', models.ForeignKey(to='cloud.Nodelist')),
            ],
            options={
                'db_table': 'thunder_Noderole',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NodeSpec',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('core', models.CharField(max_length=255)),
                ('ram', models.CharField(max_length=255)),
                ('hdd', models.CharField(max_length=255)),
                ('machine_id', models.CharField(max_length=255)),
                ('nodespec', models.ForeignKey(to='cloud.Nodelist')),
            ],
            options={
                'db_table': 'thunder_Nodespec',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recipe_name', models.CharField(max_length=255)),
                ('prority', models.IntegerField()),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'thunder_recipe',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Roletype',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role_typename', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'thunder_roletype',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service_name', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'thunder_service',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='recipe',
            name='service',
            field=models.ForeignKey(to='cloud.Service'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='noderole',
            name='role',
            field=models.ForeignKey(to='cloud.Roletype'),
            preserve_default=True,
        ),
    ]
