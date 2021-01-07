#!/usr/bin/python3
"""
Import data from CSV files into SQLite database.
"""
from include.config import logger, dbpath
from include.utils import download_dataset, read_csv
from sqlite3 import connect

conn = connect(dbpath)

logger.info('--- GOV STARTED ---')
# download_dataset()

# table `cvl`
# q = 'INSERT OR REPLACE INTO `cvl` VALUES (?, ?, ?)'
# rows = read_csv('consegne-vaccini-latest.csv')
# for row in rows:
#     pars = (row['data_consegna'], row['area'], row['numero_dosi'])
#     conn.execute(q, pars)

# table `somministrazioni_gov`
q = 'INSERT OR REPLACE INTO `somministrazioni_gov` VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
rows = read_csv('somministrazioni-vaccini-latest.csv')
for row in rows:
    pars = (row['data_somministrazione'], row['area'], row['fascia_anagrafica'], row['sesso_maschile'],
            row['sesso_femminile'], row['categoria_operatori_sanitari_sociosanitari'],
            row['categoria_personale_non_sanitario'], row['categoria_ospiti_rsa'])
    conn.execute(q, pars)

conn.commit()
logger.info('--- GOV ENDED ---')
