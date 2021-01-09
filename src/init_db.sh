#!/bin/bash
# create DESTDIR before first run
DESTDIR="/opt/vaccini/csv/"
rm -f ${DESTDIR}*.csv

# download latest CSV files
cd ${DESTDIR}
wget https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-summary-latest.csv > /dev/null 2>&1
sleep 2
wget https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/consegne-vaccini-latest.csv > /dev/null 2>&1
sleep 2
/usr/bin/python3 /opt/vaccini/app/init_db.py > /dev/null 2>&1
