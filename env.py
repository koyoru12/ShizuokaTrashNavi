import os
from __settings import SETTINGS


def import_environ():
    env = SETTINGS['env']
    os.environ['env'] = env
    for key in SETTINGS[env]:
        os.environ[key] = SETTINGS[env][key]