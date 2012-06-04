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
LANGUAGE_CODE = 'en'

EMAIL_SUBJECT_PREFIX = '[596 Acres] '
SERVER_EMAIL = 'admin@596acres.org'
ORGANIZERS_EMAIL = 'organizers@gmail.com'

TIME_ZONE = 'America/New_York'

SITE_ID = 1

USE_I18N = True
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
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',

    'sekizai.context_processors.sekizai',

    'context_processors.mobile',
    'context_processors.public_boroughs',
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
    'cms.plugins.link',
    'cms.plugins.picture',
    'cms.plugins.snippet',
    'cms.plugins.text',
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

    'about',
    'accounts',
    'fns_admin',
    'contact',
    'events',
    'facebook',
    'getinvolved',
    'legend',
    'lots',
    'news',
    'newsletter',
    'organize',
    'photos',
)

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
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

PUBLIC_BOROUGHS = [
    'Brooklyn',
]
