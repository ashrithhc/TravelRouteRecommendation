# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Clusters(models.Model):
    cluster_id = models.IntegerField(primary_key=True)
    n_user = models.IntegerField(db_column='N_user')  # Field name made lowercase.
    ic_user = models.TextField(db_column='IC_user')  # Field name made lowercase.
    content_score = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        managed = False
        db_table = 'clusters'


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Owner(models.Model):
    owner_id = models.CharField(primary_key=True, max_length=15)
    tourist = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'owner'


class Photos(models.Model):
    photo_id = models.CharField(max_length=25)
    latitude = models.CharField(max_length=10, blank=True)
    longitude = models.CharField(max_length=10, blank=True)
    owner = models.CharField(max_length=15, blank=True)
    place_id = models.CharField(max_length=25, blank=True)
    secret = models.CharField(max_length=15)
    tags = models.TextField(blank=True)
    title = models.TextField(blank=True)
    date_taken = models.DateTimeField(blank=True, null=True)
    cluster_info = models.CharField(max_length=20, blank=True)
    seed_location = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'photos'


class SeedLocation(models.Model):
    location_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    latitude1 = models.FloatField()
    longitude1 = models.FloatField()
    latitude2 = models.FloatField()
    longitude2 = models.FloatField()

    class Meta:
        managed = False
        db_table = 'seed_location'


class Temp(models.Model):
    photo_id = models.CharField(max_length=25)
    latitude = models.CharField(max_length=10, blank=True)
    longitude = models.CharField(max_length=10, blank=True)
    owner = models.CharField(max_length=15, blank=True)
    place_id = models.CharField(max_length=25, blank=True)
    secret = models.CharField(max_length=15)
    tags = models.TextField(blank=True)
    title = models.TextField(blank=True)
    date_taken = models.DateTimeField(blank=True, null=True)
    cluster_info = models.CharField(max_length=20, blank=True)
    seed_location = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'temp'
