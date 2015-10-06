# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prueba01', '0006_auto_20150825_1504'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='municipio',
            options={'ordering': ['id_edo', 'id'], 'managed': False},
        ),
    ]
