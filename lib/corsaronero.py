from lxml import html
import logging
import sys
import re
import settings
import urllib2

root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


class CorsaroNero(object):

    title = ''
    season = ''
    pattern = ''
    query = ''
    ep = 0

    def __init__(self, j):
        self.title = j['name']
        self.season = j['season']
        self.pattern = j['pattern']
        self.query = j['query']

    def find(self):
        url = self.build_url()
        tree = html.parse(urllib2.urlopen(url))
        out = self.parse_result(tree)
        print out

    def parse_result(self, tree):
        rows = tree.findall('//tr[starts-with(@class, "odd")]')
        return(rows)

    def build_url(self):
        self.ep += 1
        pagesearch = re.sub(settings.QUERY_PATTERN,
                            r'\g<1>%02d\g<2>%02d\g<3>' % (
                                self.season, self.ep),
                            self.query,
                            re.I)
        url = '{0}/{1}.html'.format(
              settings.CN_QUERY_URL,
              urllib2.quote(pagesearch))
        return(url)
