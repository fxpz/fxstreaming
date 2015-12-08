import settings
import os
import json
from lib.corsaronero import CorsaroNero

files = [x for x in os.listdir(settings.CN_PATH_JSON_FILES)
         if x.endswith('.json')]
for f in files:
    with open('{0}/{1}'.format(settings.CN_PATH_JSON_FILES, f)) as data_file:
        data = json.load(data_file)
    for j in data:
        c = CorsaroNero(j)
        c.find()
