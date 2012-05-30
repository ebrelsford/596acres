# -*- coding: utf-8 -*-
import os

gettext = lambda s: s

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

gettext = lambda s: s
LANGUAGES = [
    ('en', gettext('English')),
]
DEFAULT_LANGUAGE = 0

EMAIL_SUBJECT_PREFIX = '[596 Acres] '
SERVER_EMAIL = 'admin@596acres.org'
ORGANIZERS_EMAIL = 'organizers@gmail.com'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
STATIC_URL = "/static/"
ADMIN_MEDIA_PREFIX = "/static/admin/"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'cms.middleware.multilingual.MultilingualURLMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.debug',
    'cms.context_processors.media',
    'sekizai.context_processors.sekizai',

    'context_processors.mobile',

    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

CMS_TEMPLATES = (
    ('cms/main_template.html', 'Main Template'),
    ('cms/map_template.html', 'Map Template'),
    ('cms/breadcrumbless_template.html', 'Breadcrumbless Template'),
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.admin',
    'cms',
    'menus',
    'mptt',
    'appmedia',
    'sekizai',
    'south',
    'cms.plugins.text',
    'cms.plugins.link',
    'cms.plugins.snippet',
    'cms.plugins.googlemap',
    'tinymce',
    'compressor',

    'easy_thumbnails',
    'filer',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_image',
    'cmsplugin_filer_teaser',
    'cmsplugin_filer_video',

    'cmsplugin_blog',
    'djangocms_utils',
    'simple_translation',
    'tagging',
    'missing',
    'sorl.thumbnail',

    'about',
    'accounts',
    'fns_admin',
    'contact',
    'events',
    'getinvolved',
    'legend',
    'lots',
    'organize',
    'photos',
    'facebook',
    'news',
    'newsletter',
)

#CACHES = {
    #'default': {
        #'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        #'LOCATION': 'cache_table',
    #},
#}
#CACHE_BACKEND = 'db://cache_table'
#CACHE_MIDDLEWARE_SECONDS = 60 * 60
#CACHE_MIDDLEWARE_KEY_PREFIX = ''
#CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

CMS_CONTENT_CACHE_DURATION = 60
MENU_CACHE_DURATION = 3600

JQUERY_UI_CSS = '/media/jquery-ui/custom.css'
JQUERY_UI_JS = 'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.13/jquery-ui.min.js'
JQUERY_JS = '/media/admin/js/jquery.js'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
    'fiveninesix.finders.AppMediaDirectoriesFinder',
]
STATICFILES_DIRS = [
    '/Users/eric/Documents/activism/596acres/lib/python2.6/site-packages/cms/static',
]
ADMIN_TOOLS_INDEX_DASHBOARD = 'fiveninesix.dashboard.CustomIndexDashboard'

OASIS_BASE_URL = 'http://www.oasisnyc.net/map.aspx?etabs=1&zoomto=lot:'

TEST_RUNNER = 'ignoretests.DjangoIgnoreTestSuiteRunner'
IGNORE_TESTS = (
    'djangocms_utils',
    'south',
)

SOUTH_TESTS_MIGRATE = False

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)
