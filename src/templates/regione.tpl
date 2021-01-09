<!doctype html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
    <title>Vaccinazioni Covid-19 in __REGIONE__</title>
    <link rel="stylesheet" href="css/style.css" type="text/css" />
    <link rel="shortcut icon" type="image/x-icon" href="images/favicon.ico">
    <script src="js/utils.js"></script>
    <script src="js/Chart.min.js"></script>
</head>
<body>
    <header>Vaccinazioni Covid-19 in __REGIONE__
        <div class="comboregione dropdown">
            <button onclick="myFunction()" class="dropbtn">seleziona regione</button>
            <div id="myDropdown" class="dropdown-content">
                <a href="/">Italia</a>
                <a href="pie.html">Piemonte</a>
                <a href="vda.html">Valle d'Aosta</a>
                <a href="lom.html">Lombardia</a>
                <a href="ven.html">Veneto</a>
                <a href="fvg.html">Friuli-Venezia Giulia</a>
                <a href="lig.html">Liguria</a>
                <a href="emr.html">Emilia-Romagna</a>
                <a href="tos.html">Toscana</a>
                <a href="mar.html">Marche</a>
                <a href="umb.html">Umbria</a>
                <a href="laz.html">Lazio</a>
                <a href="abr.html">Abruzzo</a>
                <a href="mol.html">Molise</a>
                <a href="cam.html">Campania</a>
                <a href="pug.html">Puglia</a>
                <a href="bas.html">Basilicata</a>
                <a href="cal.html">Calabria</a>
                <a href="sic.html">Sicilia</a>
                <a href="sar.html">Sardegna</a>
                <a href="pab.html">P. A. Bolzano</a>
                <a href="pat.html">P. A. Trento</a>
            </div>
        </div>
    </header>
    <div class="clear"></div>
    <div class="summary">dosi: consegnate <strong>__DC__</strong> | somministrate <strong>__DS__</strong> (__DPERC__%)</div>
    <div style="width:100%;height:100%;">
		<canvas id="mygraph"></canvas>
    </div>
    <script>
    __BODY__
    </script>
    <footer>v. 0.2 - basato su dati aperti forniti dal Governo e disponibili <a href="https://github.com/italia/covid19-opendata-vaccini">qui</a> - pagine aggiornate automaticamente - <a href="https://github.com/fabiux/vaccinicovid19italia">fork me on Github!</a></footer>
</body>
</html>