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

try:
    from local_settings import *
except ImportError:
    pass

try:
    from provider_settings import *
except ImportError:
    pass
