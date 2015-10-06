# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prueba01', '0004_auto_20150825_1453'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='estado',
            options={'ordering': ['id2'], 'managed': False},
        ),
    ]
