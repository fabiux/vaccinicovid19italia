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

    def eta(self):
        """
        Restituisce il dataset (label e dati) delle somministrazioni per fascia di eta`.
        """
        if self._conn is None:
            return [], []

        q = 'SELECT `eta`, `somministrazioni` FROM `eta` WHERE `tstamp` = ? ORDER BY `eta`'
        labels = []
        data = []
        try:
            res = self._conn.execute(q, (self._lasttime, ))
            res = res.fetchall()
            for item in res:
                labels.append("'{}'".format(item[0]))
                data.append(item[1])
        except Exception as e:
            logger.error('DB.eta(): {}'.format(str(e)))

        return labels, data

    def genere(self):
        """
        Restituisce il dataset del genere.
        """
        if self._conn is None:
            return [], []

        labels = ["'maschi'", "'femmine'"]
        data = []
        q = 'SELECT `maschi`, `femmine` FROM `genere` ORDER BY `tstamp` DESC LIMIT 1'
        try:
            res = self._conn.execute(q)
            res = res.fetchone()
            data.append(res[0])
            data.append(res[1])
        except Exception as e:
            logger.error('DB.genere(): {}'.format(str(e)))

        return labels, data

    def categoria(self):
        """
        Restituisce il dataset (label e dati) delle somministrazioni per categoria.
        """
        if self._conn is None:
            return [], []

        q = 'SELECT `categoria`, `somministrazioni` FROM `categorie` WHERE `tstamp` = ? ORDER BY `categoria`'
        labels = []
        data = []
        try:
            res = self._conn.execute(q, (self._lasttime, ))
            res = res.fetchall()
            for item in res:
                labels.append("'{}'".format(item[0]))
                data.append(item[1])
        except Exception as e:
            logger.error('DB.categoria(): {}'.format(str(e)))

        return labels, data

    def _forniture(self, tstamp):
        """
        Seleziona le forniture totali di vaccini per regione fino alla data specificata.
        """
        q = 'SELECT `area`, SUM(`dosi`) FROM cvl WHERE tstamp <= ? GROUP BY `area`'
        res = self._conn.execute(q, (tstamp, ))
        dosi = dict()
        for item in res:
            dosi[item[0]] = item[1]
        return dosi

    def init_hist(self, fromdate=None):
        """
        Inizializza la tabella della serie storica temporale `somministrazioni_hist`.
        """
        if self._conn is None:
            return

        r = dict()  # transcodifica codici regioni
        q = 'SELECT `id`, `id_num` FROM `regioni_gov`'
        res = self._conn.execute(q)
        res = res.fetchall()
        for item in res:
            r[item['id']] = item['id_num']

        somm = dict(ABR=0, BAS=0, CAL=0, CAM=0, EMR=0, FVG=0, LAZ=0, LIG=0, LOM=0, MAR=0, MOL=0, PAB=0, PAT=0, PIE=0,
                    PUG=0, SAR=0, SIC=0, TOS=0, UMB=0, VDA=0, VEN=0)
        prev_tstamp = ''
        q = 'SELECT `tstamp`, `id_num`, `id_regione`, `totale` FROM `v_somministrazioni_area_gov` ORDER BY `tstamp`'
        qins = 'INSERT INTO `somministrazioni_hist` VALUES (?, ?, ?, ?, ?)'
        res = self._conn.execute(q)
        res = res.fetchall()
        for item in res:
            tstamp = item[0]
            if tstamp != prev_tstamp:
                if prev_tstamp != '':
                    # save current
                    dosi = self._forniture(tstamp)
                    for reg in somm.keys():
                        pars = (tstamp, r[item[1]], dosi[item[2]], item[3], round(item[3] / dosi[item[2]] * 100.0, 1))
                        self._conn.execute(qins, pars)
                    self._conn.commit()
                prev_tstamp = tstamp
            somm[item[2]] += item[3]
