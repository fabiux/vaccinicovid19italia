"""
Generate static website.
"""
from include.config import dbpath, tpldir, distdir
from include.chartjs import ChartJS
from sqlite3 import connect
from shutil import copyfile

conn = connect(dbpath)
body = ''

# FIXME error checking
q = 'SELECT MAX(`tstamp`) as `lasttime`, SUBSTR(MIN(`tstamp`), 1, 10) AS `firstdate` FROM `somministrazioni`'
res = conn.execute(q)
res = res.fetchone()
lasttime = res[0]
lastdate = lasttime[:10]
firstdate = res[1]

# dosi Italia
q = 'SELECT SUM(`dosi`) AS `totdosi`, SUM(`somministrazioni`) AS `totsomm` FROM `v_somministrazioni` '
q += 'WHERE `tstamp` = ?'
res = conn.execute(q, (lasttime, ))
res = res.fetchone()
dc = res[0]
ds = res[1]
dperc = round(ds / dc * 100.0, 1)

with open(tpldir + 'index.tpl', 'r') as f:
    html = f.read()
with open(tpldir + 'regione.tpl', 'r') as f:
    htmlreg = f.read()

# FIXME funzioni ad hoc
c = ChartJS('mygraph', firstdate, lastdate, chart_title='')

q = 'SELECT `somministrazioni` FROM `v_somm_day_italia` ORDER BY `tstamp`'
dsres = conn.execute(q)
dsres = dsres.fetchall()
dsres = [item[0] for item in dsres]
c.add_dataset(dsres, 'dosi', 'somministrazione', dict(r=0, g=127, b=0, a=0.2), dict(r=0, g=127, b=0, a=1.0))

q = 'SELECT `dosi` FROM `v_dosi_day_italia` ORDER BY `tstamp`'
dsres = conn.execute(q)
dsres = dsres.fetchall()
dsres = [item[0] for item in dsres]
c.add_dataset(dsres, 'fornitura', 'fornitura', dict(r=127, g=0, b=0, a=0.2), dict(r=127, g=0, b=0, a=1.0), hidden=True)

body = c.js

html = html.replace('__BODY__', body).replace('__DC__', str(dc)).replace('__DS__', str(ds))
html = html.replace('__DPERC__', str(dperc)).replace('__LASTTIME__', lasttime)

# dosi regioni
q = 'SELECT * FROM `regioni`'
res = conn.execute(q)
res = res.fetchall()
q = 'SELECT `dosi`, `somministrazioni`, `percentuale` FROM `v_somministrazioni` WHERE '
q += '(`tstamp` = ?) AND (`id_regione` = ?)'
for row in res:
    _id = row[0]
    regione = row[1]
    res2 = conn.execute(q, (lasttime, _id, ))
    res2 = res2.fetchone()
    dc = res2[0]
    ds = res2[1]
    dperc = res2[2]

    c = ChartJS('mygraph', firstdate, lastdate, chart_title='')

    q2 = 'SELECT `somministrazioni` from `v_somm_day` WHERE `id_regione` = ? ORDER BY `tstamp`'
    dsres = conn.execute(q2, (_id, ))
    dsres = dsres.fetchall()
    dsres = [item[0] for item in dsres]
    c.add_dataset(dsres, 'dosi', 'somministrazione', dict(r=0, g=127, b=0, a=0.2), dict(r=0, g=127, b=0, a=1.0))

    q2 = 'SELECT `dosi` from `v_dosi_day` WHERE `id_regione` = ? ORDER BY `tstamp`'
    dsres = conn.execute(q2, (_id, ))
    dsres = dsres.fetchall()
    dsres = [item[0] for item in dsres]
    c.add_dataset(dsres, 'fornitura', 'fornitura', dict(r=127, g=0, b=0, a=0.2), dict(r=127, g=0, b=0, a=1.0), hidden=True)

    body = c.js
    htmlreg2 = htmlreg.replace('__BODY__', body).replace('__DC__', str(dc)).replace('__DS__', str(ds))
    htmlreg2 = htmlreg2.replace('__DPERC__', str(dperc)).replace('__LASTTIME__', lasttime).replace('__REGIONE__', regione)
    with open(distdir + str(_id) + '.html', 'w') as f:
        f.write(htmlreg2)

with open(distdir + 'index.html', 'w') as f:
    f.write(html)

copyfile(tpldir + 'css/style.css', distdir + 'css/style.css')
copyfile(tpldir + 'js/utils.js', distdir + 'js/utils.js')
