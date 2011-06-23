from django.contrib.gis.db import models

class Lot(models.Model):
    objects = models.GeoManager()

    address = models.CharField(max_length=256, null=True)
    borough = models.CharField(max_length=32, null=True)
    bbl = models.CharField(max_length=32)
    block = models.CharField(max_length=32)
    lot = models.CharField(max_length=32)
    zipcode = models.CharField(max_length=16, null=True)

    owner = models.ForeignKey('Owner', null=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    school_district = models.CharField(max_length=16, null=True)
    council_district = models.CharField(max_length=16, null=True)
    council = models.CharField(max_length=16, null=True)
    fire_comp = models.CharField(max_length=16, null=True)
    health_area = models.CharField(max_length=16, null=True)
    health_ctr = models.CharField(max_length=16, null=True)
    police_precinct = models.CharField(max_length=16, null=True)
    assess_land = models.IntegerField(null=True)
    assess_total = models.IntegerField(null=True)
    exempt_land = models.IntegerField(null=True)
    exempt_total = models.IntegerField(null=True)

    centroid = models.PointField(null=True)
    centroid_source = models.CharField(max_length=32, null=True)
    polygon = models.MultiPolygonField(null=True)

class Owner(models.Model):
    name = models.CharField(max_length=256)
    phone = models.CharField(max_length=32, null=True)
    type = models.ForeignKey('OwnerType', null=True)
    code = models.CharField(max_length=8, null=True)

class OwnerType(models.Model):
    name = models.CharField(max_length=256)
