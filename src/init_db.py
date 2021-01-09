#!/usr/bin/python3
"""
Init database.
"""
from include.db import DB

db = DB()
db.init_somministrazioni()
db.refresh_forniture()
