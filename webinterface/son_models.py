# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Clients(models.Model):
    org = models.CharField(max_length=70)
    order_key = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'clients'


class DecimalNumbers(models.Model):
    mkcb = models.CharField(primary_key=True, max_length=25)
    field_name = models.CharField(db_column='_name', max_length=255, blank=True, null=True)  # Field renamed because it started with '_'.
    location = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'decimal_numbers'


class Devices(models.Model):
    serial_number = models.IntegerField(primary_key=True)
    station_number = models.ForeignKey('Stations', models.DO_NOTHING, db_column='station_number', blank=True, null=True)
    org = models.ForeignKey(Clients, models.DO_NOTHING)
    device_name = models.CharField(max_length=80)
    mkcb = models.CharField(max_length=25)
    date_out = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255)
    description_field = models.CharField(db_column='description_', max_length=50, blank=True, null=True)  # Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'devices'


class Files(models.Model):
    uuid = models.CharField(primary_key=True, max_length=64)
    parent_number = models.CharField(max_length=25)
    typef = models.CharField(max_length=3)
    namef = models.CharField(max_length=128)
    file_id = models.CharField(unique=True, max_length=128, blank=True, null=True)
    author = models.CharField(max_length=50, blank=True, null=True)
    load_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'files'


class Stations(models.Model):
    serial_number = models.IntegerField(primary_key=True)
    org = models.ForeignKey(Clients, models.DO_NOTHING)
    mkcb = models.CharField(max_length=25)
    date_out = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255)
    description_field = models.CharField(db_column='description_', max_length=50, blank=True, null=True)  # Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'stations'


class Users(models.Model):
    org = models.ForeignKey(Clients, models.DO_NOTHING)
    user_id = models.BigIntegerField(unique=True)
    user_name = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'