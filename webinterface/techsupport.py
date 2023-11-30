# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Contents(models.Model):
    parent = models.OneToOneField('Titles', models.DO_NOTHING)
    content_text = models.CharField(max_length=3000)
    location = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contents'


class Titles(models.Model):
    parent_id = models.IntegerField()
    title = models.CharField(max_length=100)
    command = models.CharField(unique=True, max_length=50, blank=True, null=True)
    title_type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'titles'
