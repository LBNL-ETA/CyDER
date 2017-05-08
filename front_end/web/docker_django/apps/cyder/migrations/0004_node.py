# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cyder', '0003_usermodel_simulation_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('node_id', models.CharField(max_length=50, null=True, blank=True)),
                ('section_id', models.CharField(max_length=50, null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('model', models.ForeignKey(blank=True, to='cyder.Model', null=True)),
            ],
        ),
    ]
