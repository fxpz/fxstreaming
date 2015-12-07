import settings
from lxml import html
import urllib2
import re
import sys
import logging

root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


class PsManiaco(object):

    page_file_name = ''
    raw_content = ''
    content = ''
    title = ''
    tree = ''
    raw_items = []
    season = 0
    password = ''

    def __init__(self, pfn):
        self.page_file_name = pfn
        url = 'file://{0}/{1}'.format(settings.PSM_PATH_PAGE_FILES, pfn)
        self.tree = html.parse(urllib2.urlopen(url))
        logging.info('open %s' % pfn)
        logging.debug('url %s' % url)
        self.init_logging()
        self.init_data()

    def init_logging(self):
        if settings.LOGFILE == '':
            logging.basicConfig(level=settings.LOGLEVEL)
        else:
            logging.basicConfig(filename=settings.LOGDIR+settings.LOGFILE,
                                level=settings.LOGLEVEL)

    def init_data(self):
        self.fetch_links()
        self.fetch_content()
        self.fetch_title()

    def fetch_links(self):
        links = self.tree.xpath(settings.PSM_XPATH_HREF)
        mega_link = []
        for link in links:
            if link.attrib['href'].startswith('https://mega.'):
                mega_link.append({'text': link.text_content(),
                                 'href': link.attrib['href']})
        self.raw_items = mega_link

    def fetch_content(self):
        content = self.tree.findall(settings.PSM_XPATH_CONTENT)[0]
        for br in content.xpath("*//br"):
            br.tail = "\n" + br.tail if br.tail else "\n"
        self.raw_content = content.text_content()
        self.init_content()

    def fetch_title(self):
        title = self.tree.xpath(settings.PSM_XPATH_TITLE)[0]
        self.raw_title = title.text_content()
        self.init_title()

    def getRawContent(self):
        return(self.raw_content)

    def getRawItems(self):
        return(self.raw_items)

    def getRawTitle(self):
        return(self.raw_title)

    def getTitle(self):
        return(self.title)

    def getSeason(self):
        return(self.season)

    def getContent(self):
        return(self.content)

    def getPassword(self):
        return(self.password)

    def getRawItemsName(self):
        items = [x['text'] for x in self.raw_items]
        return(items)

    def getRawItemsUrl(self):
        items = [x['href'] for x in self.raw_items]
        return(items)

    def init_title(self):
        title = self.raw_title
        for regex in settings.PSM_TITLE_FILTER_OUT:
            title = re.sub(regex[0], regex[1], title, flags=re.I)

        for regex in settings.PSM_SEASON_NUMERIC_REGEX:
            r = re.match(regex[0], title, flags=re.I)
            if r:
                self.title = r.group(regex[1]).strip()
                self.season = r.group(regex[2])
                break
        if self.season == 0:
            logging.warning('no regex matched "%s"' % title)

    def init_content(self):
        content = unicode(self.raw_content).split("\n")
        self.content = content
        for row in content:
            for regex in settings.PSM_PASSWORD_REGEX:
                r = re.match(regex[0], row, re.I)
                if r:
                    self.password = r.group(regex[1])
                    logging.info('password found')
                    break
