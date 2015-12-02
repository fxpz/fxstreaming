import settings
import os
from lib.psmaniaco import PsManiaco

files = [x for x in os.listdir(settings.PSM_PATH_PAGE_FILES)
         if x.endswith('.html')]
for f in files:
    p = PsManiaco(f)
    print p.getRawTitle()
    print p.getRawContent()
    print "---------------------------\n"
