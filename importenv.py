import os
from __settings import SETTINGS

for key in SETTINGS:
    print(key)
    os.environ[key] = SETTINGS[key]