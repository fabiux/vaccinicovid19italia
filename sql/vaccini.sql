DROP TABLE IF EXISTS `regioni`;
CREATE TABLE `regioni` (
    `id` INTEGER NOT NULL,
    `description` VARCHAR(21) NOT NULL,
    PRIMARY KEY (`id`)
);
INSERT INTO `regioni` VALUES (1, 'Piemonte');
INSERT INTO `regioni` VALUES (2, "Valle d'Aosta");
INSERT INTO `regioni` VALUES (3, 'Lombardia'); -- il codice 4 non e` utilizzato
INSERT INTO `regioni` VALUES (5, 'Veneto');
INSERT INTO `regioni` VALUES (6, 'Friuli-Venezia Giulia');
INSERT INTO `regioni` VALUES (7, 'Liguria');
INSERT INTO `regioni` VALUES (8, 'Emilia-Romagna');
INSERT INTO `regioni` VALUES (9, 'Toscana');
INSERT INTO `regioni` VALUES (10, 'Umbria');
INSERT INTO `regioni` VALUES (11, 'Marche');
INSERT INTO `regioni` VALUES (12, 'Lazio');
INSERT INTO `regioni` VALUES (13, 'Abruzzo');
INSERT INTO `regioni` VALUES (14, 'Molise');
INSERT INTO `regioni` VALUES (15, 'Campania');
INSERT INTO `regioni` VALUES (16, 'Puglia');
INSERT INTO `regioni` VALUES (17, 'Basilicata');
INSERT INTO `regioni` VALUES (18, 'Calabria');
INSERT INTO `regioni` VALUES (19, 'Sicilia');
INSERT INTO `regioni` VALUES (20, 'Sardegna');
INSERT INTO `regioni` VALUES (21, 'P.A. Bolzano');
INSERT INTO `regioni` VALUES (22, 'P.A. Trento');

DROP TABLE IF EXISTS `somministrazioni`;
CREATE TABLE `somministrazioni` ( -- somministrazioni.csv
    `tstamp` CHAR(19) NOT NULL, -- aggiornamento
    `regione` INTEGER NOT NULL, -- codice_regione
    `dosi` INTEGER NOT NULL, -- dosiConsegnate
    `somministrazioni` INTEGER NOT NULL, -- somministrazioni
    `percentuale` REAL NOT NULL, -- campo calcolato
    PRIMARY KEY (`tstamp`, `regione`)
);

DROP TABLE IF EXISTS `categorie`;
CREATE TABLE `categorie` ( -- categoria.csv
    `tstamp` CHAR(19) NOT NULL, -- aggiornamento
    `categoria` VARCHAR(40) NOT NULL, -- categoria
    `somministrazioni` INTEGER NOT NULL, -- vaccinazioni
    PRIMARY KEY (`tstamp`, `categoria`)
);

DROP TABLE IF EXISTS `eta`;
CREATE TABLE `eta` ( -- fasceEta.csv
    `tstamp` CHAR(19) NOT NULL, -- aggiornamento
    `eta` VARCHAR(5) NOT NULL, -- fascia
    `somministrazioni` INTEGER NOT NULL, -- vaccinazioni
    PRIMARY KEY (`tstamp`, `eta`)
);

DROP TABLE IF EXISTS `genere`;
CREATE TABLE `genere` ( -- sesso.csv
    `tstamp` CHAR(19) NOT NULL, -- aggiornamento
    `maschi` INTEGER NOT NULL, -- maschi
    `femmine` INTEGER NOT NULL, -- femmine
    PRIMARY KEY (`tstamp`)
);
