# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cyder', '0010_auto_20170130_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='result_available',
            field=models.BooleanField(default=False),
        ),
    ]
