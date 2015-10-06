# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prueba01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_mun', models.IntegerField()),
                ('nombre', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'municipio',
                'managed': False,
            },
        ),
    ]
