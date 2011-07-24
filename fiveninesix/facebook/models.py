from django.db import models

from cms.models import CMSPlugin

class FacebookAccount(models.Model):
    facebookId = models.CharField(max_length=64)

    def __unicode__(self):
        return self.facebookId

class FacebookPhotoPlugin(CMSPlugin):
    account = models.ForeignKey(FacebookAccount)
    width = models.IntegerField(blank=True, null=True)

    def copy_relations(self, oldinstance):
        self.account = oldinstance.account
        self.save()

class FacebookLikeboxPlugin(CMSPlugin):
    url = models.URLField()

    def __unicode__(self):
        return self.url
