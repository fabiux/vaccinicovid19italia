"""
Configuration.
"""
from logging import getLogger, Formatter, DEBUG  # log level [NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL]
from logging.handlers import RotatingFileHandler

csvdir = '/opt/vaccini/csv/'
tpldir = '/opt/vaccini/app/templates/'
distdir = '/opt/vaccini/dist/'
dbpath = '/opt/vaccini/vaccini.db'
alpha = 0.1

# logging
logname = 'vaccini'
logfile = "/opt/vaccini/logs/app.log"
loglevel = DEBUG
logformat = "%(asctime)s %(levelname)-8s %(message)s"
logdateformat = "%Y-%m-%d %H:%M:%S"
logmaxbytes = 4096000  # log max size
logbkpcount = 1  # log max backup copies
logger = getLogger(logname)
handler = RotatingFileHandler(logfile, maxBytes=logmaxbytes, backupCount=logbkpcount)
formatter = Formatter(logformat, datefmt=logdateformat)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(loglevel)
