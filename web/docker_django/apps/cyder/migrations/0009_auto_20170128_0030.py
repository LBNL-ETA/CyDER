# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cyder', '0008_noderesult'),
    ]

    operations = [
        migrations.AddField(
            model_name='noderesult',
            name='distance',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='noderesult',
            name='latitude',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='noderesult',
            name='longitude',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
