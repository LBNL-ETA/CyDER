# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cyder', '0013_electricvehiclescenario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electricvehiclescenario',
            name='usermodel',
            field=models.OneToOneField(null=True, blank=True, to='cyder.UserModel'),
        ),
        migrations.AlterField(
            model_name='noderesult',
            name='usermodel',
            field=models.OneToOneField(null=True, blank=True, to='cyder.UserModel'),
        ),
    ]
