from os.path import dirname
from os.path  import join

ROOT_URLCONF = None

ROOT_PATH = dirname(__file__)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".  Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

    join(ROOT_PATH, 'templates'),
)
