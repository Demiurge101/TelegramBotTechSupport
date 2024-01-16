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


    def __str__(self):
        return f"{self.parent}: {self.content_text} ({self.location})"



    class Meta:
        managed = False
        db_table = 'contents'


class Filebond(models.Model):
    bond_id = models.AutoField(primary_key=True)
    title_id = models.IntegerField()
    uuid = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        managed = False
        db_table = 'filebond'


class Files(models.Model):
    uuid = models.CharField(primary_key=True, max_length=64)
    namef = models.CharField(max_length=128)
    file_id = models.CharField(unique=True, max_length=128, blank=True, null=True)
    author = models.CharField(max_length=50, blank=True, null=True)
    load_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.namef}: {self.author} ({self.load_date})"

    class Meta:
        managed = False
        db_table = 'files'

    # def set_name(self, name):
    #     self.fields['namef'] = name


class Titles(models.Model):
    title_id = models.AutoField(primary_key=True)
    parent_id = models.IntegerField()
    title = models.CharField(max_length=100)
    command = models.CharField(unique=True, max_length=50, blank=True, null=True)
    title_type = models.IntegerField()

    def __str__(self):
        return f"{self.title_id}){self.title} ({self.parent_id}): {self.command} <{self.title_type}>"

    class Meta:
        managed = False
        db_table = 'titles'
