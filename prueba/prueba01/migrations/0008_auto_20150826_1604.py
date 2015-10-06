# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prueba01', '0007_auto_20150825_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='Centro',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=256)),
                ('direccion', models.CharField(max_length=256)),
                ('mesas', models.IntegerField(null=True, blank=True)),
                ('electores', models.IntegerField(null=True, blank=True)),
                ('venezolanos', models.IntegerField(null=True, blank=True)),
                ('extranjeros', models.IntegerField(null=True, blank=True)),
                ('circuitos_15', models.IntegerField(null=True, blank=True)),
                ('focal', models.NullBooleanField()),
                ('latitud', models.CharField(max_length=32, null=True, blank=True)),
                ('longitud', models.CharField(max_length=32, null=True, blank=True)),
            ],
            options={
                'ordering': ['id'],
                'db_table': 'centro',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Parroquia',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=64)),
            ],
            options={
                'ordering': ['id'],
                'db_table': 'parroquia',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('nac', models.CharField(max_length=1)),
                ('ci', models.IntegerField()),
                ('nombre1', models.CharField(max_length=64)),
                ('nombre2', models.CharField(max_length=64, null=True, blank=True)),
                ('apellido1', models.CharField(max_length=64)),
                ('apellido2', models.CharField(max_length=64, null=True, blank=True)),
                ('fecha_nac', models.DateField()),
                ('sexo', models.CharField(max_length=1)),
                ('ecivil', models.IntegerField()),
                ('ipp', models.IntegerField(null=True, blank=True)),
                ('estrato', models.CharField(max_length=1, null=True, blank=True)),
                ('isei', models.FloatField(null=True, blank=True)),
                ('id', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
                'ordering': ['nac', 'ci'],
                'db_table': 'persona',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='municipio',
            options={'ordering': ['id'], 'managed': False},
        ),
    ]
