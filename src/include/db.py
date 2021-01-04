"""
Class DB.
"""
from include.config import logger, dbpath
from sqlite3 import connect


class DB(object):
    def __init__(self):
        self._conn = None
        self._firsttime = None
        self._lasttime = None
        self._firstdate = None
        self._lastdate = None

        try:
            self._conn = connect(dbpath)
        except Exception as e:
            logger.error('DB.__init__() [1]: {}'.format(str(e)))
            return

        # time bounds
        q = 'SELECT MIN(`tstamp`) AS `firstdtime`, MAX(`tstamp`) as `lastdtime` FROM `somministrazioni`'
        try:
            res = self._conn.execute(q)
            res = res.fetchone()
            self._firsttime = res[0]
            self._lasttime = res[1]
            self._firstdate = self._firsttime[:10]
            self._lastdate = self._lasttime[:10]
        except Exception as e:
            logger.error('DB.__init__() [2]: {}'.format(str(e)))

    @property
    def firstdate(self):
        return self._firstdate

    @property
    def lastdate(self):
        return self._lastdate

    @property
    def lasttime(self):
        return self._lasttime

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
            q = 'SELECT SUM(`dosi`) AS `totdosi`, SUM(`somministrazioni`) AS `totsomm` FROM `v_somministrazioni` '
            q += 'WHERE `tstamp` = ?'
            res = self._conn.execute(q, (self._lasttime, ))
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

        q = 'SELECT `dosi`, `somministrazioni`, `percentuale` FROM `v_somministrazioni` WHERE '
        q += '(`tstamp` = ?) AND (`id_regione` = ?)'
        try:
            res = self._conn.execute(q, (self._lasttime, id_regione, ))
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

        q = 'SELECT `somministrazioni` from `v_somm_day` WHERE `id_regione` = ? ORDER BY `tstamp`'
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

        q = 'SELECT `dosi` from `v_dosi_day` WHERE `id_regione` = ? ORDER BY `tstamp`'
        try:
            res = self._conn.execute(q, (id_regione, ))
            res = res.fetchall()
            return [item[0] for item in res]
        except Exception as e:
            logger.error('DB.ds_forn_regione(): {}'.format(str(e)))
            return []
