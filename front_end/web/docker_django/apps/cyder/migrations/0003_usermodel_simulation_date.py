# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cyder', '0002_usermodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='simulation_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
