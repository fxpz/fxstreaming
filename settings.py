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
EP_PATTERN_REGEX = [
    r'^\D+(?P<season>\d+)\D+(?P<start>\d+)(-|_|\ )(?P<end>\d+).*$',
    r'^\D+(?P<season>\d+)\D+(?P<start>\d+)\D+.*$'
]

SEEDS_THRESHOLD = 100
RETRY_NORES = 2

try:
    from local_settings import *
except ImportError:
    pass

try:
    from provider_settings import *
except ImportError:
    pass
