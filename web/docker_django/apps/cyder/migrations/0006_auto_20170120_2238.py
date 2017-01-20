# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cyder', '0005_devices'),
    ]

    operations = [
        migrations.RenameField(
            model_name='calibrationresult',
            old_name='impedance_a',
            new_name='impedance',
        ),
        migrations.RemoveField(
            model_name='calibrationresult',
            name='impedance_b',
        ),
        migrations.RemoveField(
            model_name='calibrationresult',
            name='impedance_c',
        ),
    ]
