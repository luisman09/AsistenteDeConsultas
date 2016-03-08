# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Estado(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=64)

    def __unicode__(self):
        return str(self.id) + " " + self.nombre

    class Meta:
        managed = False
        db_table = 'estado'
        ordering = ['id']


class Municipio(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=64)
    id_edo = models.ForeignKey(Estado, db_column='id_edo')

    def __unicode__(self):
        return str(self.id) + " " + self.nombre

    class Meta:
        managed = False
        db_table = 'municipio'
        ordering = ['id']


class Parroquia(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=64)
    id_mun = models.ForeignKey(Municipio, db_column='id_mun')

    def __unicode__(self):
        return str(self.id) + " " + self.nombre

    class Meta:
        managed = False
        db_table = 'parroquia'
        ordering = ['id']


class Centro(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=256)
    circuitos_15 = models.IntegerField(blank=True, null=True)
    id_parr = models.ForeignKey(Parroquia, db_column='id_parr')

    def __unicode__(self):
        return str(self.id) + " " + self.nombre

    class Meta:
        managed = False
        db_table = 'centro'
        ordering = ['id']