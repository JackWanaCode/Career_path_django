from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_5=#=+cl&lp@&ayps6ia0viff)^v$_wvutyyxca!xu0w6d2z3$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


ALLOWED_HOSTS = ['192.168.1.124', '54.183.221.146', '192.168.1.105', 'localhost', '127.0.0.1', 'jackwanacode.website']

EMAIL_BACKEND = 'django.app.mail.backends.console.EmailBackend'

SERVER_EMAIL = 'infooveriq@gmail.com'
DEFAULT_FROM_EMAIL = SERVER_EMAIL

ADMINS = (
    ('OverIQ', 'admin@overiq.com'),
)

MANAGERS = (
    ('OverIQ', 'manager@overiq.com'),
)
