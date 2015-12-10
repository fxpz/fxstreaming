from settings import *
from lxml import html
import logging
import sys
import re
import urllib2
import humanfriendly
import time

root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
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
    founds = []

    def __init__(self, j):
        self.init_logging()
        self.title = j['name']
        self.season = j['season']
        self.pattern = j['pattern']
        self.query = j['query']
        logging.info('creadet object for show: %s %s' % (self.title,
                     self.season))

    def init_logging(self):
        if LOGFILE == '':
            logging.basicConfig(level=LOGLEVEL)
        else:
            logging.basicConfig(filename=LOGDIR + LOGFILE,
                                level=LOGLEVEL)

    def find(self):
        search = True
        while search:
            res = self.find_ep()
            search = res['continue']
        logging.info('%s %s searching finished' % (self.title, self.season))

    def find_ep(self):
        url = self.build_url()
        logging.debug('calling url %s' % url)
        try:
            url_content = urllib2.urlopen(url)
        except urllib2.HTTPError:
            logging.error('invalid url')
            return({'found': False, 'continue': False})

        tree = html.parse(url_content)
        results = self.parse_result(tree)
        if len(results) > 0:
            self.tryed = 0
            result = self.filter_results(results)
            self.ep = int(result['ep_end'])
            logging.info('found ep from %d to %d' %
                         (int(result['ep_start']), self.ep))
            self.founds.append(result)
            return({'found': True, 'continue': True})
        else:
            if self.ep > 1 and self.tryed <= RETRY_NORES:
                logging.warning('ep %d not found. Try to find ep %d' %
                                (self.ep, self.ep + 1))
                self.tryed += 1
                return({'found': False, 'continue': True})
            else:
                if self.ep == 1:
                    logging.error('Ep 1 not found. Stop searching')
                else:
                    logging.warning('Tried %d times. Stop searching' %
                                    self.tryed)
                return({'found': False, 'continue': False})

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
            return([])

    def filter_results(self, items):
        filtered = [k for k in items if int(k['seeds']) >= SEEDS_THRESHOLD]
        if len(filtered) == 0:
            logging.warning('ep %d not found enough seeds. Use full results' % self.ep)
            filtered = items
        ordered = sorted(filtered, key=lambda k: k['size'], reverse=True)
        return(ordered[0])

    def build_url(self):
        self.ep += 1
        logging.debug('building url for S%sE%s' % (self.season, self.ep))
        pagesearch = re.sub(QUERY_PATTERN,
                            r'\g<1>%02d\g<2>%02d\g<3>' % (
                                self.season, self.ep),
                            self.query,
                            re.I)
        url = '{0}/{1}.html'.format(
              CN_QUERY_URL,
              urllib2.quote(pagesearch))
        return(url)
