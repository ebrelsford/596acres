from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class PhotosApphook(CMSApp):
    name = _("Photos Apphook")
    urls = ('photos.urls_app',)

apphook_pool.register(PhotosApphook)
