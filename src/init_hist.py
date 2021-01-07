"""
Init hist tables.
"""
from include.config import logger, dbpath
from sqlite3 import connect

conn = connect(dbpath)
