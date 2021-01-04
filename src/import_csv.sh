#!/bin/bash
# create DESTDIR before first run
DESTDIR="/opt/vaccini/csv/"
rm -f ${DESTDIR}*.csv

# download latest CSV files
cd ${DESTDIR}
wget https://raw.githubusercontent.com/ondata/covid19italia/master/webservices/vaccini/processing/somministrazioni.csv > /dev/null 2>&1
sleep 2
wget https://raw.githubusercontent.com/ondata/covid19italia/master/webservices/vaccini/processing/fasceEta.csv > /dev/null 2>&1
sleep 2
wget https://raw.githubusercontent.com/ondata/covid19italia/master/webservices/vaccini/processing/categoria.csv > /dev/null 2>&1
sleep 2
wget https://raw.githubusercontent.com/ondata/covid19italia/master/webservices/vaccini/processing/sesso.csv > /dev/null 2>&1
sleep 2
/usr/bin/python3 /opt/vaccini/app/import_csv.py > /dev/null 2>&1
/usr/bin/python3 /opt/vaccini/app/gen_static_site.py > /dev/null 2>&1
