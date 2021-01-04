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
dc, ds = db.dosi_italia()
if dc is None:
    exit()
dperc = round(ds / dc * 100.0, 1)

c.add_dataset(db.ds_somm_italia(), 'dosi', 'somministrazione', dict(r=0, g=127, b=0, a=alpha), dict(r=0, g=127, b=0, a=1.0))
c.add_dataset(db.ds_forn_italia(), 'fornitura', 'fornitura', dict(r=127, g=0, b=0, a=alpha), dict(r=127, g=0, b=0, a=1.0), hidden=True)

html = read_template('index')
html = html.replace('__BODY__', c.js).replace('__DC__', str(dc)).replace('__DS__', str(ds))
html = html.replace('__DPERC__', str(dperc)).replace('__LASTTIME__', db.lasttime)
write_html('index', html)

# fasce di eta`
htmlbar = read_template('bar')
labels, data = db.eta()
if labels != []:
    c = ChartJS('mygraph', db.firstdate, db.lastdate, chart_title='', chart_type='bar', labels=labels)
    c.add_dataset(data, 'eta', 'eta', dict(r=0, g=0, b=192, a=alphabar), dict(r=0, g=0, b=192, a=1.0))
    html = htmlbar.replace('__DATASEL__', 'Fasce di età').replace('__BODY__', c.js).replace('__DC__', str(dc)).replace('__DS__', str(ds))
    html = html.replace('__DPERC__', str(dperc)).replace('__LASTTIME__', db.lasttime)
    write_html('eta', html)

# genere
labels, data = db.genere()
if data != []:
    c = ChartJS('mygraph', db.firstdate, db.lastdate, chart_title='', chart_type='bar', labels=labels)
    c.add_dataset(data, 'genere', 'genere', dict(r=192, g=64, b=0, a=alphabar), dict(r=192, g=64, b=0, a=1.0))
    html = htmlbar.replace('__DATASEL__', 'Genere').replace('__BODY__', c.js).replace('__DC__', str(dc)).replace('__DS__', str(ds))
    html = html.replace('__DPERC__', str(dperc)).replace('__LASTTIME__', db.lasttime)
    write_html('genere', html)

# categorie
labels, data = db.categoria()
if labels != []:
    c = ChartJS('mygraph', db.firstdate, db.lastdate, chart_title='', chart_type='bar', labels=labels)
    c.add_dataset(data, 'categoria', 'categoria', dict(r=64, g=192, b=0, a=alphabar), dict(r=64, g=192, b=0, a=1.0))
    html = htmlbar.replace('__DATASEL__', 'Categoria lavorativa').replace('__BODY__', c.js).replace('__DC__', str(dc)).replace('__DS__', str(ds))
    html = html.replace('__DPERC__', str(dperc)).replace('__LASTTIME__', db.lasttime)
    write_html('categoria', html)

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
    c.add_dataset(db.ds_somm_regione(_id), 'dosi', 'somministrazione', dict(r=0, g=127, b=0, a=alpha), dict(r=0, g=127, b=0, a=1.0))
    c.add_dataset(db.ds_forn_regione(_id), 'fornitura', 'fornitura', dict(r=127, g=0, b=0, a=alpha), dict(r=127, g=0, b=0, a=1.0), hidden=True)

    html = htmlreg.replace('__BODY__', c.js).replace('__DC__', str(dc)).replace('__DS__', str(ds))
    html = html.replace('__DPERC__', str(dperc)).replace('__LASTTIME__', db.lasttime).replace('__REGIONE__', regione)
    write_html(str(_id), html)

copyfile(tpldir + 'css/style.css', distdir + 'css/style.css')
copyfile(tpldir + 'js/utils.js', distdir + 'js/utils.js')

logger.info('--- ENDED ---')
