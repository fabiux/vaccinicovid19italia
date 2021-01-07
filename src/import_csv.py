"""
Import data from CSV files into SQLite database.
"""
from include.config import dbpath
from include.utils import read_csv
from sqlite3 import connect
from datetime import datetime


def tstamp(tstamp):
    """
    Convert timestamp to 'YYYY-MM-DD HH:MM:SS'.
    """
    tstamp = tstamp.split(' ')
    d = tstamp[0].split('/')
    t = tstamp[1].split(':')
    hour = int(t[0])
    if tstamp[2] == 'PM':
        hour += 12
    else:
        if hour == 12:
            hour = 0
    return str(datetime(int(d[2]), int(d[0]), int(d[1]), hour, int(t[1]), int(t[2])))


conn = connect(dbpath)

# table `somministrazioni`
q = 'INSERT OR IGNORE INTO `somministrazioni` VALUES (?, ?, ?, ?, ?)'
rows = read_csv('somministrazioni.csv')
for row in rows:
    percent = round(float(row['somministrazioni']) / float(row['dosiConsegnate']) * 100.0, 1)
    pars = (tstamp(row['aggiornamento']), row['codice_regione'], row['dosiConsegnate'], row['somministrazioni'], percent)
    conn.execute(q, pars)

# table `categorie`
q = 'INSERT OR IGNORE INTO `categorie` VALUES (?, ?, ?)'
rows = read_csv('categoria.csv')
for row in rows:
    pars = (tstamp(row['aggiornamento']), row['categoria'], row['vaccinazioni'])
    conn.execute(q, pars)

# table `eta`
q = 'INSERT OR IGNORE INTO `eta` VALUES (?, ?, ?)'
rows = read_csv('fasceEta.csv')
for row in rows:
    pars = (tstamp(row['aggiornamento']), row['fascia'], row['vaccinazioni'])
    conn.execute(q, pars)

# table `genere`
q = 'INSERT OR IGNORE INTO `genere` VALUES (?, ?, ?)'
rows = read_csv('sesso.csv')
for row in rows:
    pars = (tstamp(row['aggiornamento']), row['maschi'], row['femmine'])
    conn.execute(q, pars)

conn.commit()
