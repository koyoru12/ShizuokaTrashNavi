import os
from __settings import SETTINGS

def import_environ():
    for key in SETTINGS:
        os.environ[key] = SETTINGS[key]