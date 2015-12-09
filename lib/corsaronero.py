from settings import *
from lxml import html
import logging
import sys
import re
import urllib2
import humanfriendly
import time

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
    tryed = 0

    def __init__(self, j):
        self.init_logging()
        self.title = j['name']
        self.season = j['season']
        self.pattern = j['pattern']
        self.query = j['query']
        logging.info('find show: %s %s' % (self.title, self.season))

    def init_logging(self):
        if LOGFILE == '':
            logging.basicConfig(level=LOGLEVEL)
        else:
            logging.basicConfig(filename=LOGDIR + LOGFILE,
                                level=LOGLEVEL)

    def find(self):
        url = self.build_url()
        logging.debug('calling url %s' % url)
        tree = html.parse(urllib2.urlopen(url))
        results = self.parse_result(tree)
        if results:
            self.tryed = 0
            result = self.filter_results(results)
            if result:
                self.ep = int(result['ep_end'])
                print result
                self.find()
        else:
            if self.ep > 1 and self.tryed >= RETRY_NORES:
                self.ep += 1
                self.tryed += 1
                self.find()
            else:
                logging.info('no more result found')
                return(False)

    def parse_result(self, tree):
        rows = tree.xpath(CN_XPATH_RESULTS_ROWS)
        if len(rows) >= 1:
            logging.debug('found %d rows' % len(rows))
            results = []
            for row in rows:
                result = {}
                tds = row.getchildren()
                a = tds[1].find('.//a[@href]')
                ep_found = 1
                for regex in EP_PATTERN_REGEX:
                    r = re.match(regex, a.text_content())
                    if r:
                        result['season'] = r.group('season')
                        result['ep_start'] = r.group('start')
                        result['ep_end'] = result['ep_start']
                        if 'end' in regex:
                            result['ep_end'] = r.group('end')
                            ep_found = int(result['ep_end']) - int(result['ep_start'])
                            if ep_found == 0:
                                ep_found = 1
                        break
                result['text'] = a.text_content()
                result['link'] = a.attrib['href']
                result['size'] = humanfriendly.parse_size(tds[2].text_content()) / ep_found
                result['data'] = time.strptime(tds[4].text_content(), "%d.%m.%y")
                result['seeds'] = int(tds[5].text_content())
                result['leech'] = int(tds[6].text_content())
                item_tree = html.parse(urllib2.urlopen(result['link']))
                links = item_tree.xpath('//a[@href]')
                for link in links:
                        if link.attrib['href'].startswith('magnet:?'):
                            result['torrent'] = link.attrib['href']
                results.append(result)
            return(results)
        else:
            return(False)

    def filter_results(self, items):
        filtered = [k for k in items if int(k['seeds']) > SEEDS_THRESHOLD]
        if len(filtered) == 0:
            filtered = items
        ordered = sorted(items, key=lambda k: k['size'], reverse=True)
        return(ordered[0])

    def build_url(self):
        self.ep += 1
        logging.warning('finding ep %s' % self.ep)
        pagesearch = re.sub(QUERY_PATTERN,
                            r'\g<1>%02d\g<2>%02d\g<3>' % (
                                self.season, self.ep),
                            self.query,
                            re.I)
        url = '{0}/{1}.html'.format(
              CN_QUERY_URL,
              urllib2.quote(pagesearch))
        return(url)
