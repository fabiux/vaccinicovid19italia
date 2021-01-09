#!/usr/bin/python3
"""
Import data from CSV files into SQLite database.
"""
from include.config import logger
from include.db import DB

logger.info('--- data import STARTED ---')
db = DB()
db.update_somministrazioni()
db.refresh_forniture()
logger.info('--- data import ENDED ---')
