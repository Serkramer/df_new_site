# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Areas(models.Model):
    ref = models.CharField(primary_key=True, max_length=36, verbose_name='id')
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Назва області")
    description_ru = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'areas'
        verbose_name = 'Область'
        verbose_name_plural = 'Області'

    def __str__(self):
        return self.description


class PostOffices(models.Model):
    ref = models.CharField(primary_key=True, max_length=36)
    delivery_fr = models.CharField(max_length=12, blank=True, null=True)
    delivery_mo = models.CharField(max_length=12, blank=True, null=True)
    delivery_sa = models.CharField(max_length=12, blank=True, null=True)
    delivery_su = models.CharField(max_length=12, blank=True, null=True)
    delivery_th = models.CharField(max_length=12, blank=True, null=True)
    delivery_tu = models.CharField(max_length=12, blank=True, null=True)
    delivery_we = models.CharField(max_length=12, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='Адреса')
    description_ru = models.CharField(max_length=255, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True, verbose_name="номер відділення")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    place_max_weight_allowed = models.IntegerField(blank=True, null=True, verbose_name='максимальна вага')
    reception_fr = models.CharField(max_length=12, blank=True, null=True)
    reception_mo = models.CharField(max_length=12, blank=True, null=True)
    reception_sa = models.CharField(max_length=12, blank=True, null=True)
    reception_su = models.CharField(max_length=12, blank=True, null=True)
    reception_th = models.CharField(max_length=12, blank=True, null=True)
    reception_tu = models.CharField(max_length=12, blank=True, null=True)
    reception_we = models.CharField(max_length=12, blank=True, null=True)
    schedule_fr = models.CharField(max_length=12, blank=True, null=True)
    schedule_mo = models.CharField(max_length=12, blank=True, null=True)
    schedule_sa = models.CharField(max_length=12, blank=True, null=True)
    schedule_su = models.CharField(max_length=12, blank=True, null=True)
    schedule_th = models.CharField(max_length=12, blank=True, null=True)
    schedule_tu = models.CharField(max_length=12, blank=True, null=True)
    schedule_we = models.CharField(max_length=12, blank=True, null=True)
    short_address = models.CharField(max_length=255, blank=True, null=True, verbose_name='коротка адреса')
    short_address_ru = models.CharField(max_length=255, blank=True, null=True)
    site_key = models.CharField(max_length=100, blank=True, null=True)
    total_max_weight_allowed = models.IntegerField(blank=True, null=True)
    settlement = models.ForeignKey('Settlements', models.DO_NOTHING, blank=True, null=True, verbose_name="населенний пункт")

    class Meta:
        managed = False
        db_table = 'post_offices'
        verbose_name = 'Вдділення'
        verbose_name_plural = 'Вдділення'

    def __str__(self):
        return f"НП-{self.number}, {self.short_address}"


class Regions(models.Model):
    ref = models.CharField(primary_key=True, max_length=36)
    description = models.CharField(max_length=255, blank=True, null=True)
    description_ru = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'regions'


class Settlements(models.Model):
    ref = models.CharField(primary_key=True, max_length=36)
    delivery_fr = models.TextField(blank=True, null=True)  # This field type is a guess.
    delivery_mo = models.TextField(blank=True, null=True)  # This field type is a guess.
    delivery_sa = models.TextField(blank=True, null=True)  # This field type is a guess.
    delivery_su = models.TextField(blank=True, null=True)  # This field type is a guess.
    delivery_th = models.TextField(blank=True, null=True)  # This field type is a guess.
    delivery_tu = models.TextField(blank=True, null=True)  # This field type is a guess.
    delivery_we = models.TextField(blank=True, null=True)  # This field type is a guess.
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='Адреса')
    description_ru = models.CharField(max_length=255, blank=True, null=True)
    index1 = models.IntegerField()
    index2 = models.IntegerField()
    indexcoatsu1 = models.BigIntegerField()
    latitude = models.CharField(max_length=18, blank=True, null=True)
    longitude = models.CharField(max_length=18, blank=True, null=True)
    warehouse = models.TextField(blank=True, null=True)  # This field type is a guess.
    area_ref = models.ForeignKey(Areas, models.DO_NOTHING, db_column='area_ref', blank=True, null=True)
    region_ref = models.ForeignKey(Regions, models.DO_NOTHING, db_column='region_ref', blank=True, null=True)
    settlement_type_ref = models.ForeignKey('SettlementsType', models.DO_NOTHING, db_column='settlement_type_ref', blank=True, null=True)
    last_update_post_office = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'settlements'
        verbose_name = 'Населений пункт'
        verbose_name_plural = 'Населені пункти'

    def __str__(self):
        return f"{self.description}"


class SettlementsType(models.Model):
    ref = models.CharField(primary_key=True, max_length=36)
    description = models.CharField(max_length=255, blank=True, null=True)
    description_ru = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'settlements_type'
