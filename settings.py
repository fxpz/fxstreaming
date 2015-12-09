import logging

# PATH
ROOT_PATH = '/home/fxstreaming/fxstreaming'
FILES_PATH = '%s/files' % ROOT_PATH 

# LOGGING
LOGDIR = '/tmp/'
LOGFILE = 'fxlog'
LOGLEVEL = logging.DEBUG

# PATTERN
QUERY_PATTERN = r'^([^\*]+)\*+([^\*]+)\*+([^\*]+)$'

# PSMANIACO
PSM_PATH_PAGE_FILES = '%s/psmaniaco' % FILES_PATH

PSM_XPATH_HREF = '//a[@href]'
PSM_XPATH_CONTENT = '//table[@class="color"]'
PSM_XPATH_TITLE = '/html/head/title'

PSM_TITLE_FILTER_OUT = [
    ('\[ita\]', ''),
    ('serie\ tv', ''),
    ('\ {2}', ' '),
    ('-', '')
]

PSM_SEASON_NUMERIC_REGEX = [
    (r'^(.*)(stagione|serie)\ (\d)+.*$', 1, 3),
]

PSM_SEASON_LITERAL_REGEX = [
    (r'^(.*)(prima|seconda|terza|quarta|quinta|sesta|settima|'
     'ottava|nona|decima)\ (stagione).*$', 1, 2),
    (r'^(.*)(stagione)\ (uno|due|tre|quattro|cinque|sei|sette|'
     'otto|nove|dieci).*$', 1, 3),
]

PSM_PASSWORD_REGEX = [
    (r'^.*(password).*:\ *(.*)$', 2)
]

CN_PATH_JSON_FILES = '%s/corsaronero' % FILES_PATH
CN_QUERY_URL = 'http://ilcorsaronero.info/torrent-ita/15'
CN_XPATH_RESULTS_ROWS = '//div[@id="left"][@class="left"]/table/tr/td[2]/table/tr[starts-with(@class,"odd")]'
