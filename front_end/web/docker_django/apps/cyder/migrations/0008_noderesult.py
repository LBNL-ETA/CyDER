# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cyder', '0007_auto_20170125_2013'),
    ]

    operations = [
        migrations.CreateModel(
            name='NodeResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('node_id', models.CharField(max_length=50, null=True, blank=True)),
                ('voltage_A', models.FloatField(null=True, blank=True)),
                ('voltage_B', models.FloatField(null=True, blank=True)),
                ('voltage_C', models.FloatField(null=True, blank=True)),
                ('usermodel', models.ForeignKey(blank=True, to='cyder.UserModel', null=True)),
            ],
        ),
    ]
