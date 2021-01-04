"""
Generate static website.
"""
from include.config import logger, tpldir, distdir, alpha
from include.db import DB
from include.chartjs import ChartJS
from shutil import copyfile

logger.info('--- STARTED ---')

db = DB()
if db.lastdate is None:
    exit()

body = ''
c = ChartJS('mygraph', db.firstdate, db.lastdate, chart_title='')
with open(tpldir + 'index.tpl', 'r') as f:
    html = f.read()
with open(tpldir + 'regione.tpl', 'r') as f:
    htmlreg = f.read()

# dosi Italia
dc, ds = db.dosi_italia()
if dc is None:
    exit()
dperc = round(ds / dc * 100.0, 1)

c.add_dataset(db.ds_somm_italia(), 'dosi', 'somministrazione', dict(r=0, g=127, b=0, a=alpha), dict(r=0, g=127, b=0, a=1.0))
c.add_dataset(db.ds_forn_italia(), 'fornitura', 'fornitura', dict(r=127, g=0, b=0, a=alpha), dict(r=127, g=0, b=0, a=1.0), hidden=True)

body = c.js

html = html.replace('__BODY__', body).replace('__DC__', str(dc)).replace('__DS__', str(ds))
html = html.replace('__DPERC__', str(dperc)).replace('__LASTTIME__', db.lasttime)

# dosi regioni
regioni = db.regioni()
if regioni is None:
    exit()

for row in regioni:
    _id = row[0]
    regione = row[1]
    dc, ds, dperc = db.ds_regione(_id)
    if dc is None:
        continue

    c = ChartJS('mygraph', db.firstdate, db.lastdate, chart_title='')
    c.add_dataset(db.ds_somm_regione(_id), 'dosi', 'somministrazione', dict(r=0, g=127, b=0, a=alpha), dict(r=0, g=127, b=0, a=1.0))
    c.add_dataset(db.ds_forn_regione(_id), 'fornitura', 'fornitura', dict(r=127, g=0, b=0, a=alpha), dict(r=127, g=0, b=0, a=1.0), hidden=True)

    body = c.js
    htmlreg2 = htmlreg.replace('__BODY__', body).replace('__DC__', str(dc)).replace('__DS__', str(ds))
    htmlreg2 = htmlreg2.replace('__DPERC__', str(dperc)).replace('__LASTTIME__', db.lasttime).replace('__REGIONE__', regione)
    with open(distdir + str(_id) + '.html', 'w') as f:
        f.write(htmlreg2)

with open(distdir + 'index.html', 'w') as f:
    f.write(html)

copyfile(tpldir + 'css/style.css', distdir + 'css/style.css')
copyfile(tpldir + 'js/utils.js', distdir + 'js/utils.js')

logger.info('--- ENDED ---')
