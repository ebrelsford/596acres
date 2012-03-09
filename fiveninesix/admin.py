from django.contrib import admin
from django.core.urlresolvers import reverse

from settings import OASIS_BASE_URL

class LotRelatedModelAdmin(admin.ModelAdmin):
    """
    Adds handy links for models with a Lot ForeignKey relationship.

    Make sure you add 'view_lot' or 'view_in_oasis' to list_display in the child ModelAdmin.
    """
    def view_lot(self, obj):
        return _view_lot(obj.lot)
    view_lot.allow_tags = True

    def view_in_oasis(self, obj):
        return _view_in_oasis(obj.lot)
    view_in_oasis.allow_tags = True

def _view_lot(lot):
    """
    A link to open the given lot on the site.
    """
    return '<a target="_blank" href="%s">%s</a>' % (reverse('lots.views.details', kwargs={ 'bbl': lot.bbl }), lot.bbl,)

def _view_in_oasis(lot):
    """
    A link to open the given lot in OASIS.
    """
    return '<a target="_blank" href="%s%s">OASIS</a>' % (OASIS_BASE_URL, lot.bbl)
