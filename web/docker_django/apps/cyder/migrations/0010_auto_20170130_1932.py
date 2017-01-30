# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cyder', '0009_auto_20170128_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='in_progress',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='status',
            field=models.TextField(null=True, blank=True),
        ),
    ]
