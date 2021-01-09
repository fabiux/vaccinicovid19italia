"""
Class DB.
"""
from include.config import logger, dbpath, regcodes
from include.utils import read_csv
from sqlite3 import connect
from datetime import datetime, timedelta


class DB(object):
    def __init__(self):
        self._conn = None
        self._firstdate = None
        self._lastdate = None

        try:
            self._conn = connect(dbpath)
        except Exception as e:
            logger.error('DB.__init__() [1]: {}'.format(str(e)))
            return

        # time bounds
        q = 'SELECT MIN(`tstamp`) AS `firstdate`, MAX(`tstamp`) as `lastdate` FROM `somministrazioni`'
        try:
            res = self._conn.execute(q)
            res = res.fetchone()
            self._firstdate = res[0]
            self._lastdate = res[1]
        except Exception as e:
            logger.error('DB.__init__() [2]: {}'.format(str(e)))

    @property
    def firstdate(self):
        return self._firstdate

    @property
    def lastdate(self):
        return self._lastdate

    def _next_tstamp(self, tstamp):
        currdt = datetime(int(tstamp[:4]), int(tstamp[5:7]), int(tstamp[8:]), 0, 0, 0)
        return str(currdt + timedelta(days=1))[:10]

    def regioni(self):
        """
        Restituisce il dataset delle regioni (id, description).
        """
        if self._conn is None:
            return []

        try:
            q = 'SELECT * FROM `regioni`'
            res = self._conn.execute(q)
            return res.fetchall()
        except Exception as e:
            logger.error('DB.regioni(): {}'.format(str(e)))
            return None

    def dosi_italia(self):
        """
        Restituisce, nell'ordine, dosi fornite e somministrate in tutta Italia.
        """
        if self._conn is None:
            return None, None
        try:
            q = 'SELECT SUM(`dosi`) AS `totdosi`, SUM(`somministrazioni`) AS `totsomm`, `percentuale` '
            q += 'FROM `v_somministrazioni` WHERE `tstamp` = ?'
            res = self._conn.execute(q, (self._lastdate, ))
            return res.fetchone()
        except Exception as e:
            logger.error('DB.dosi_italia(): {}'.format(str(e)))
            return None, None

    def ds_somm_italia(self):
        """
        Restituisce il dataset (list) delle somministrazioni - Italia
        """
        if self._conn is None:
            return []

        q = 'SELECT `somministrazioni` FROM `v_somm_day_italia` ORDER BY `tstamp`'
        try:
            res = self._conn.execute(q)
            res = res.fetchall()
            return [item[0] for item in res]
        except Exception as e:
            logger.error('DB.ds_somm_italia(): {}'.format(str(e)))
            return []

    def ds_forn_italia(self):
        """
        Restituisce il dataset (list) delle forniture - Italia
        """
        if self._conn is None:
            return []

        q = 'SELECT `dosi` FROM `v_dosi_day_italia` ORDER BY `tstamp`'
        try:
            res = self._conn.execute(q)
            res = res.fetchall()
            return [item[0] for item in res]
        except Exception as e:
            logger.error('DB.ds_forn_italia(): {}'.format(str(e)))
            return []

    def ds_regione(self, id_regione):
        """
        Restituisce i dati regionali; nell'ordine: dosi fornite, dosi somministrate, percentuale di somministrazione.
        """
        if self._conn is None:
            return None, None, None

        q = 'SELECT `dosi`, `somministrazioni`, `percentuale` FROM `v_somministrazioni` WHERE (`id_regione` = ?) '
        q += 'ORDER BY `tstamp` DESC LIMIT 1'
        try:
            res = self._conn.execute(q, (id_regione, ))
            res = res.fetchone()
            return res
        except Exception as e:
            logger.error('DB.ds_regione(): {}'.format(str(e)))
            return None, None, None

    def ds_somm_regione(self, id_regione):
        """
        Restituisce il dataset (list) delle somministrazioni - regione
        """
        if self._conn is None:
            return []

        q = 'SELECT `somministrazioni` from `somministrazioni` WHERE `regione` = ? ORDER BY `tstamp`'
        try:
            res = self._conn.execute(q, (id_regione, ))
            res = res.fetchall()
            return [item[0] for item in res]
        except Exception as e:
            logger.error('DB.ds_somm_regione(): {}'.format(str(e)))
            return []

    def ds_forn_regione(self, id_regione):
        """
        Restituisce il dataset (list) delle forniture - regione
        """
        if self._conn is None:
            return []

        q = 'SELECT `dosi` from `somministrazioni` WHERE `regione` = ? ORDER BY `tstamp`'
        try:
            res = self._conn.execute(q, (id_regione, ))
            res = res.fetchall()
            return [item[0] for item in res]
        except Exception as e:
            logger.error('DB.ds_forn_regione(): {}'.format(str(e)))
            return []

    def _fornitura(self, tstamp, regione):
        """
        Restituisce la fornitura totale di vaccini di una regione a una certa data.
        """
        if self._conn is None:
            return 0

        try:
            q = 'SELECT SUM(`dosi`) FROM `forniture` WHERE (`tstamp` <= ?) AND (`regione` = ?)'
            res = self._conn.execute(q, (tstamp, regione))
            res = res.fetchone()
            return res[0]
        except Exception as e:
            logger.error('DB._fornitura(): {}'.format(str(e)))
            return 0

    def _fix_somministrazioni(self, startdate='2020-12-27'):
        """
        Riempie possibili buchi della tabella `somministrazioni`.
        """
        if self._conn is None:
            return

        def set_regioni(tstamp):
            q = 'SELECT `regione` FROM `somministrazioni` WHERE `tstamp` = ?'
            res = self._conn.execute(q, (tstamp, ))
            res = res.fetchall()
            return [item[0] for item in res]

        def somm_regione(tstamp, reg):
            q = 'SELECT MAX(`somministrazioni`) AS `somm` FROM `somministrazioni` '
            q += 'WHERE (`tstamp` < ?) AND (`regione` = ?) '
            res = self._conn.execute(q, (tstamp, reg))
            res = res.fetchone()
            return res[0]

        def update_somm_regione(tstamp, reg, value):
            q = 'INSERT INTO `somministrazioni` (`tstamp`, `regione`, `somministrazioni`) VALUES (?, ?, ?)'
            self._conn.execute(q, (tstamp, reg, value))

        currdate = startdate
        today = str(datetime.now())[:10]
        while currdate <= today:
            sr = set_regioni(currdate)
            for reg in regcodes:
                if reg not in sr:
                    somm = 0 if currdate == '2020-12-27' else somm_regione(currdate, reg)
                    update_somm_regione(currdate, reg, somm)
            currdate = self._next_tstamp(currdate)
        self._conn.commit()

    def init_somministrazioni(self):
        """
        Inizializza la tabella `somministrazioni`.
        """
        if self._conn is None:
            return

        tots = dict()
        for reg in regcodes:
            tots[reg] = 0

        try:
            self._conn.execute('DELETE FROM `somministrazioni`')
            q = 'INSERT INTO `somministrazioni` (`tstamp`, `regione`, `somministrazioni`) VALUES (?, ?, ?)'
            rows = read_csv('somministrazioni-vaccini-summary-latest.csv')
            for row in rows:
                if row['area'] == 'ITA':
                    continue
                tot = int(row['totale']) + tots[row['area']]
                tots[row['area']] = tot
                pars = (row['data_somministrazione'], row['area'], tot)
                self._conn.execute(q, pars)
            self._fix_somministrazioni()
            self._conn.commit()
        except Exception as e:
            logger.error('DB.init_somministrazioni(): {}'.format(str(e)))
            self._conn.rollback()

    def refresh_forniture(self):
        """
        Ricostruisce la tabella `forniture`.
        """
        if self._conn is None:
            return

        try:
            self._conn.execute('DELETE FROM `forniture`')
            q = 'INSERT INTO `forniture` VALUES (?, ?, ?)'
            rows = read_csv('consegne-vaccini-latest.csv')
            for row in rows:
                pars = (row['data_consegna'], row['area'], row['numero_dosi'])
                self._conn.execute(q, pars)

            today = str(datetime.now())[:10]
            tstart = '2020-12-27'
            currtime = tstart
            while currtime <= today:
                for reg in regcodes:
                    self._conn.execute('UPDATE `somministrazioni` SET `dosi` = ? WHERE (`tstamp` = ?) AND (`regione` = ?)',
                                       (self._fornitura(currtime, reg), currtime, reg))
                currtime = self._next_tstamp(currtime)
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            logger.error('DB.refresh_forniture(): {}'.format(str(e)))

    def update_somministrazioni(self):
        """
        Aggiorna la tabella `somministrazioni`.
        """
        if self._conn is None:
            return

        yesterday = str(datetime.now() + timedelta(days=1))[:10]

        q = 'INSERT OR REPLACE INTO `somministrazioni` VALUES (?, ?, ?, ?)'
        rows = read_csv('somministrazioni-vaccini-summary-latest.csv')
        try:
            for row in rows:
                if row['data_somministrazione'] >= yesterday:
                    pars = (row['data_somministrazione'], row['area'], self._fornitura(row['data_somministrazione'], row['area']),
                            row['totale'])
                    self._conn.execute(q, pars)
            self._fix_somministrazioni(startdate=yesterday)
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            logger.error('DB.update_somministrazioni(): {}'.format(str(e)))
