#!/usr/bin/python3
"""
Generate static website.
"""
from include.config import logger, alpha, alphabar, tpldir, distdir
from include.utils import read_template, write_html
from include.db import DB
from include.chartjs import ChartJS
from shutil import copyfile

logger.info('--- STARTED ---')

db = DB()
if db.lastdate is None:
    exit()

c = ChartJS('mygraph', db.firstdate, db.lastdate, chart_title='')

# dosi Italia
dc, ds, dperc = db.dosi_italia()
if dc is None:
    exit()

c.add_dataset(db.ds_forn_italia(), 'fornitura', 'fornitura', dict(r=127, g=0, b=0, a=alpha), dict(r=127, g=0, b=0, a=1.0), hidden=True)
c.add_dataset(db.ds_somm_italia(), 'somministrazioni', 'somministrazioni', dict(r=0, g=127, b=0, a=alpha), dict(r=0, g=127, b=0, a=1.0))

html = read_template('index')
html = html.replace('__BODY__', c.js).replace('__DC__', str(dc)).replace('__DS__', str(ds))
html = html.replace('__DPERC__', str(dperc))
write_html('index', html)

# dosi regioni
regioni = db.regioni()
if regioni is None:
    exit()

htmlreg = read_template('regione')
for row in regioni:
    _id = row[0]
    regione = row[1]
    dc, ds, dperc = db.ds_regione(_id)
    if dc is None:
        continue

    c = ChartJS('mygraph', db.firstdate, db.lastdate, chart_title='')
    c.add_dataset(db.ds_forn_regione(_id), 'fornitura', 'fornitura', dict(r=127, g=0, b=0, a=alpha), dict(r=127, g=0, b=0, a=1.0), hidden=True)
    c.add_dataset(db.ds_somm_regione(_id), 'somministrazioni', 'somministrazioni', dict(r=0, g=127, b=0, a=alpha), dict(r=0, g=127, b=0, a=1.0))

    html = htmlreg.replace('__BODY__', c.js).replace('__DC__', str(dc)).replace('__DS__', str(ds))
    html = html.replace('__DPERC__', str(dperc)).replace('__REGIONE__', regione)
    write_html(_id.lower(), html)

copyfile(tpldir + 'css/style.css', distdir + 'css/style.css')
copyfile(tpldir + 'js/utils.js', distdir + 'js/utils.js')

# easter egg
html = read_template('molise')
write_html('molise', html)

logger.info('--- ENDED ---')
