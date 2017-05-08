# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cyder', '0006_auto_20170120_2238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calibrationresult',
            name='impedance',
        ),
        migrations.AddField(
            model_name='calibrationresult',
            name='impedance_imag',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='calibrationresult',
            name='impedance_real',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
