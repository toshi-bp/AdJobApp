import os

#settings.pyからそのままコピーした
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'django-insecure-#eo)f446apy$gkbn8!38=)^^4_b_e77iqhla6l#(c!2g_70fd3'

#settings.pyからそのままコピーした
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = True # ローカルではデバッグが行われるようになる