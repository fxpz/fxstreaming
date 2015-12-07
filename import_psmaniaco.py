import settings
import os
from lib.psmaniaco import PsManiaco

files = [x for x in os.listdir(settings.PSM_PATH_PAGE_FILES)
         if x.endswith('.html')]
for f in files:
    p = PsManiaco(f)
    print p.getTitle()
    print p.getSeason()
    print p.getPassword()
    print p.getRawItems()[-1]['text']
