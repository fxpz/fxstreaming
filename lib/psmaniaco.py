import settings

from lxml import html
import urllib


class PsManiaco(object):

    page_file_name = ''
    raw_content = ''
    content = ''
    title = ''
    tree = ''
    raw_items = []

    def __init__(self, pfn):
        self.page_file_name = pfn
        url = 'file://{0}/{1}'.format(settings.PSM_PATH_PAGE_FILES, pfn)
        self.content = urllib.urlopen(url).read()
        self.tree = html.fromstring(self.content)
        self.init_data()

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
        description_found = True
        content = self.tree.xpath('{0}/{1}'.format(
            settings.PSM_XPATH_CONTENT, '/text()'))
        if not any('Titolo' in s for s in content):
            content = self.tree.xpath('{0}'.format(
                settings.PSM_XPATH_CONTENT))[0].text_content()
            description_found = False
        self.description_found = description_found
        self.raw_content = content

    def fetch_title(self):
        title = self.tree.xpath('{0}/{1}'.format(
            settings.PSM_XPATH_TITLE, '/text()'))
        self.raw_title = title

    def getRawContent(self):
        if self.description_found:
            return(self.raw_content)
        else:
            return([])

    def getRawItems(self):
        return(self.raw_items)

    def getRawTitle(self):
        return(self.raw_title)

    def getRawItemsName(self):
        items = [x['text'] for x in self.raw_items]
        return(items)

    def getRawItemsUrl(self):
        items = [x['href'] for x in self.raw_items]
        return(items)
