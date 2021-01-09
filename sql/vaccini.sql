CREATE TABLE `regioni` (
    `id` CHAR(3) NOT NULL,
    `description` VARCHAR(21) NOT NULL,
    PRIMARY KEY (`id`)
);
INSERT INTO `regioni` VALUES ('PIE', 'Piemonte');
INSERT INTO `regioni` VALUES ('VDA', "Valle d'Aosta");
INSERT INTO `regioni` VALUES ('LOM', 'Lombardia'); -- il codice 4 non e` utilizzato
INSERT INTO `regioni` VALUES ('VEN', 'Veneto');
INSERT INTO `regioni` VALUES ('FVG', 'Friuli-Venezia Giulia');
INSERT INTO `regioni` VALUES ('LIG', 'Liguria');
INSERT INTO `regioni` VALUES ('EMR', 'Emilia-Romagna');
INSERT INTO `regioni` VALUES ('TOS', 'Toscana');
INSERT INTO `regioni` VALUES ('UMB', 'Umbria');
INSERT INTO `regioni` VALUES ('MAR', 'Marche');
INSERT INTO `regioni` VALUES ('LAZ', 'Lazio');
INSERT INTO `regioni` VALUES ('ABR', 'Abruzzo');
INSERT INTO `regioni` VALUES ('MOL', 'Molise');
INSERT INTO `regioni` VALUES ('CAM', 'Campania');
INSERT INTO `regioni` VALUES ('PUG', 'Puglia');
INSERT INTO `regioni` VALUES ('BAS', 'Basilicata');
INSERT INTO `regioni` VALUES ('CAL', 'Calabria');
INSERT INTO `regioni` VALUES ('SIC', 'Sicilia');
INSERT INTO `regioni` VALUES ('SAR', 'Sardegna');
INSERT INTO `regioni` VALUES ('PAB', 'P.A. Bolzano');
INSERT INTO `regioni` VALUES ('PAT', 'P.A. Trento');

DROP TABLE IF EXISTS `somministrazioni`;
CREATE TABLE `somministrazioni` (
    `tstamp` CHAR(19) NOT NULL,
    `regione` CHAR(3) NOT NULL,
    `dosi` INTEGER NOT NULL DEFAULT 0,
    `somministrazioni` INTEGER NOT NULL,
    PRIMARY KEY (`tstamp`, `regione`)
);

DROP TABLE IF EXISTS `forniture`;
CREATE TABLE `forniture` (
    `tstamp` CHAR(19) NOT NULL,
    `regione` CHAR(3) NOT NULL,
    `dosi` INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (`tstamp`, `regione`)
);