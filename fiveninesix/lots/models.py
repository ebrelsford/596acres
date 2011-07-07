from django.contrib.gis.db import models

class Lot(models.Model):
    objects = models.GeoManager()

    address = models.CharField(max_length=256, null=True, blank=True)
    borough = models.CharField(max_length=32, null=True, blank=True)
    bbl = models.CharField(max_length=32)
    block = models.CharField(max_length=32)
    lot = models.CharField(max_length=32)
    zipcode = models.CharField(max_length=16, null=True, blank=True)

    owner = models.ForeignKey('Owner', null=True, blank=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    school_district = models.CharField(max_length=16, null=True, blank=True)
    council_district = models.CharField(max_length=16, null=True, blank=True)
    council = models.CharField(max_length=16, null=True, blank=True)
    fire_comp = models.CharField(max_length=16, null=True, blank=True)
    health_area = models.CharField(max_length=16, null=True, blank=True)
    health_ctr = models.CharField(max_length=16, null=True, blank=True)
    police_precinct = models.CharField(max_length=16, null=True, blank=True)
    assess_land = models.IntegerField(null=True, blank=True)
    assess_total = models.IntegerField(null=True, blank=True)
    exempt_land = models.IntegerField(null=True, blank=True)
    exempt_total = models.IntegerField(null=True, blank=True)

    is_vacant = models.BooleanField(default=True)
    actual_use = models.CharField(max_length=128, null=True, blank=True)

    centroid = models.PointField(null=True)
    centroid_source = models.CharField(max_length=32, null=True, blank=True)
    polygon = models.MultiPolygonField(null=True, blank=True)

class Owner(models.Model):
    name = models.CharField(max_length=256)
    person = models.CharField(max_length=128, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    site = models.URLField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    type = models.ForeignKey('OwnerType', null=True, blank=True)
    code = models.CharField(max_length=8, null=True, blank=True)

    def __unicode__(self):
        return self.name

class OwnerType(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name
