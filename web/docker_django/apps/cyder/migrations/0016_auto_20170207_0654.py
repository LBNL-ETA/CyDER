# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cyder', '0015_auto_20170206_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noderesult',
            name='usermodel',
            field=models.ForeignKey(blank=True, to='cyder.UserModel', null=True),
        ),
    ]
