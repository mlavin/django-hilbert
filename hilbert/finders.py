from django.core.exceptions import ImproperlyConfigured

try:
    from django.contrib.staticfiles.finders import AppDirectoriesFinder
    from django.contrib.staticfiles.storage import AppStaticStorage
except ImportError:
    raise ImproperlyConfigured('AppMediaDirectoriesFinder can only be used with Django 1.3 or higher.')


class AppMediaStorage(AppStaticStorage):
    source_dir = 'media'


class AppMediaDirectoriesFinder(AppDirectoriesFinder):
    storage_class = AppMediaStorage
