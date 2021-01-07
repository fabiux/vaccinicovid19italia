DROP TABLE IF EXISTS `regioni_gov`;
CREATE TABLE `regioni_gov` (
    `id` CHAR(3) NOT NULL,
    `description` VARCHAR(21) NOT NULL,
    `id_num` INTEGER NOT NULL,  -- `id` tabella `regioni`
    PRIMARY KEY (`id`)
);
INSERT INTO `regioni_gov` VALUES ('PIE', 'Piemonte', 1);
INSERT INTO `regioni_gov` VALUES ('VDA', "Valle d'Aosta", 2);
INSERT INTO `regioni_gov` VALUES ('LOM', 'Lombardia', 3); -- il codice 4 non e` utilizzato
INSERT INTO `regioni_gov` VALUES ('VEN', 'Veneto', 5);
INSERT INTO `regioni_gov` VALUES ('FVG', 'Friuli-Venezia Giulia', 6);
INSERT INTO `regioni_gov` VALUES ('LIG', 'Liguria', 7);
INSERT INTO `regioni_gov` VALUES ('EMR', 'Emilia-Romagna', 8);
INSERT INTO `regioni_gov` VALUES ('TOS', 'Toscana', 9);
INSERT INTO `regioni_gov` VALUES ('UMB', 'Umbria', 10);
INSERT INTO `regioni_gov` VALUES ('MAR', 'Marche', 11);
INSERT INTO `regioni_gov` VALUES ('LAZ', 'Lazio', 12);
INSERT INTO `regioni_gov` VALUES ('ABR', 'Abruzzo', 13);
INSERT INTO `regioni_gov` VALUES ('MOL', 'Molise', 14);
INSERT INTO `regioni_gov` VALUES ('CAM', 'Campania', 15);
INSERT INTO `regioni_gov` VALUES ('PUG', 'Puglia', 16);
INSERT INTO `regioni_gov` VALUES ('BAS', 'Basilicata', 17);
INSERT INTO `regioni_gov` VALUES ('CAL', 'Calabria', 18);
INSERT INTO `regioni_gov` VALUES ('SIC', 'Sicilia', 19);
INSERT INTO `regioni_gov` VALUES ('SAR', 'Sardegna', 20);
INSERT INTO `regioni_gov` VALUES ('PAB', 'P.A. Bolzano', 21);
INSERT INTO `regioni_gov` VALUES ('PAT', 'P.A. Trento', 22);

-- fornitura vaccini per data e area
DROP TABLE IF EXISTS `cvl`;
CREATE TABLE `cvl` ( -- consegne-vaccini-latest.csv
	`tstamp` CHAR(19) NOT NULL, -- data_consegna
	`area` CHAR(3) NOT NULL, -- area
	`dosi` INTEGER NOT NULL, -- numero_dosi
	PRIMARY KEY (`tstamp`, `area`)
);

-- somministrazioni per data e area
DROP TABLE IF EXISTS `somministrazioni_gov`;
CREATE TABLE `somministrazioni_gov` ( -- somministrazioni-vaccini-latest.csv
	`tstamp` CHAR(19) NOT NULL, -- data_somministrazione
	`area` CHAR(3) NOT NULL, -- area
	`eta` VARCHAR(5) NOT NULL, -- fascia_anagrafica
	`m` INTEGER NOT NULL, -- sesso_maschile
	`f` INTEGER NOT NULL, -- sesso_femminile
	`oss` INTEGER NOT NULL, -- categoria_operatori_sanitari_sociosanitari
	`pns` INTEGER NOT NULL, -- categoria_personale_non_sanitario
	`rsa` INTEGER NOT NULL, -- categoria_ospiti_rsa
	PRIMARY KEY (`tstamp`, `area`, `eta`)
);

-- somministrazioni - serie storica che replica la precedente tabella `somministrazioni`
DROP TABLE IF EXISTS `somministrazioni_hist`;
CREATE TABLE `somministrazioni_hist` (
	`tstamp` CHAR(19) NOT NULL,
	`regione` INTEGER NOT NULL,
	`dosi` INTEGER NOT NULL,
    `somministrazioni` INTEGER NOT NULL,
    `percentuale` REAL NOT NULL,
    PRIMARY KEY (`tstamp`, `regione`)
);

-- totale fornitura attuale per regione
DROP VIEW IF EXISTS `v_fornitura_current`;
CREATE VIEW `v_fornitura_current` AS SELECT
`cvl`.`area` AS `id_regione`,
`r`.`description` AS `regione`,
SUM(`cvl`.`dosi`) AS `dosi`
FROM `cvl`
LEFT JOIN `regioni_gov` AS `r`
ON `cvl`.`area` = `r`.`id`
GROUP BY `cvl`.`area`;

-- somministrazioni per eta` e area
DROP VIEW IF EXISTS `v_somministrazioni_eta_gov`;
CREATE VIEW `v_somministrazioni_eta_gov` AS SELECT
`s`.`tstamp` AS `tstamp`,
`s`.`area` AS `id_regione`,
`r`.`description` AS `regione`,
`r`.`id_num` AS `id_num`,
`s`.`eta` AS `eta`,
`s`.`m` AS `m`,
`s`.`f` AS `f`,
`s`.`m` + `s`.`f` AS `totale`
FROM `somministrazioni_gov` AS `s`
LEFT JOIN `regioni_gov` AS `r`
ON `s`.`area` = `r`.`id`
ORDER BY `tstamp`, `area`;

-- somministrazioni per area
DROP VIEW IF EXISTS `v_somministrazioni_area_gov`;
CREATE VIEW `v_somministrazioni_area_gov` AS SELECT
`s`.`tstamp` AS `tstamp`,
`s`.`id_regione` AS `id_regione`,
`s`.`regione` AS `regione`,
`s`.`id_num` AS `id_num`,
SUM(`s`.`m`) AS `m`,
SUM(`s`.`f`) AS `f`,
SUM(`s`.`m`) + SUM(`s`.`f`) AS `totale`
FROM `v_somministrazioni_eta_gov` AS `s`
GROUP BY `tstamp`, `id_regione`;

-- somministrazioni (Italia)
DROP VIEW IF EXISTS `v_somministrazioni_gov`;
CREATE VIEW `v_somministrazioni_gov` AS SELECT
`s`.`tstamp` AS `tstamp`,
SUM(`s`.`m`) AS `m`,
SUM(`s`.`f`) AS `f`,
SUM(`s`.`m`) + SUM(`s`.`f`) AS `totale`
FROM `v_somministrazioni_area_gov` AS `s`
GROUP BY `tstamp`;
