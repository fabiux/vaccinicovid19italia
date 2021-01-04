DROP VIEW IF EXISTS `v_somministrazioni`;
CREATE VIEW `v_somministrazioni` AS SELECT
`s`.`tstamp` AS `tstamp`,
`r`.`id` AS `id_regione`,
`r`.`description` AS `regione`,
`s`.`dosi` AS `dosi`,
`s`.`somministrazioni` AS `somministrazioni`,
`s`.`percentuale` AS `percentuale`
FROM `somministrazioni` AS `s`
LEFT JOIN `regioni` AS `r` ON `s`.`regione` = `r`.`id`
ORDER BY `tstamp` DESC, `regione` ASC;

DROP VIEW IF EXISTS `v_somm_day`;
CREATE VIEW `v_somm_day` AS SELECT
SUBSTR(`s`.`tstamp`, 1, 10) AS `tstamp`,
`s`.`id_regione` AS `id_regione`,
MAX(`s`.`somministrazioni`) AS `somministrazioni`
FROM `v_somministrazioni` AS `s`
GROUP BY SUBSTR(`s`.`tstamp`, 1, 10), `id_regione`
ORDER BY `tstamp`;

DROP VIEW IF EXISTS `v_somm_day_italia`;
CREATE VIEW `v_somm_day_italia` AS SELECT
`s`.`tstamp` AS `tstamp`,
SUM(`s`.`somministrazioni`) AS `somministrazioni`
FROM `v_somm_day` AS `s`
GROUP BY `tstamp`
ORDER BY `tstamp`;

DROP VIEW IF EXISTS `v_dosi_day`;
CREATE VIEW `v_dosi_day` AS SELECT
SUBSTR(`s`.`tstamp`, 1, 10) AS `tstamp`,
`s`.`id_regione` AS `id_regione`,
MAX(`s`.`dosi`) AS `dosi`
FROM `v_somministrazioni` AS `s`
GROUP BY SUBSTR(`s`.`tstamp`, 1, 10), `id_regione`
ORDER BY `tstamp`;

DROP VIEW IF EXISTS `v_dosi_day_italia`;
CREATE VIEW `v_dosi_day_italia` AS SELECT
`s`.`tstamp` AS `tstamp`,
SUM(`s`.`dosi`) AS `dosi`
FROM `v_dosi_day` AS `s`
GROUP BY `tstamp`
ORDER BY `tstamp`;