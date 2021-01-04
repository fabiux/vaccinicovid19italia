<!doctype html>
<html>
<head>
    <meta charset="utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
    <title>Vaccinazioni Covid-19 in __REGIONE__</title>
    <link rel="stylesheet" href="css/style.css" type="text/css" />
    <link rel="shortcut icon" type="image/x-icon" href="/favicon.ico">
    <script src="js/utils.js"></script>
    <script src="js/Chart.min.js"></script>
</head>
<body>
    <header>Vaccinazioni Covid-19 in __REGIONE__
        <div class="comboregione dropdown">
            <button onclick="myFunction()" class="dropbtn">seleziona regione</button>
            <div id="myDropdown" class="dropdown-content">
                <a href="/">Italia</a>
                <a href="1.html">Piemonte</a>
                <a href="2.html">Valle d'Aosta</a>
                <a href="3.html">Lombardia</a>
                <a href="5.html">Veneto</a>
                <a href="6.html">Friuli-Venezia Giulia</a>
                <a href="7.html">Liguria</a>
                <a href="8.html">Emilia-Romagna</a>
                <a href="9.html">Toscana</a>
                <a href="10.html">Marche</a>
                <a href="11.html">Umbria</a>
                <a href="12.html">Lazio</a>
                <a href="13.html">Abruzzo</a>
                <a href="14.html">Molise</a>
                <a href="15.html">Campania</a>
                <a href="16.html">Puglia</a>
                <a href="17.html">Basilicata</a>
                <a href="18.html">Calabria</a>
                <a href="19.html">Sicilia</a>
                <a href="20.html">Sardegna</a>
                <a href="21.html">P. A. Bolzano</a>
                <a href="22.html">P. A. Trento</a>
            </div>
        </div>
    </header>
    <div class="clear"></div>
    <div class="summary">dosi: consegnate <strong>__DC__</strong> | somministrate <strong>__DS__</strong> (__DPERC__%) - aggiornamento: __LASTTIME__</div>
    <div style="width:100%;height:100%;">
		<canvas id="mygraph"></canvas>
    </div>
    <script>
    __BODY__
    </script>
    <footer>v. 0.1 - basato su dati liberati da <strong><a href="https://ondata.it/">onData</a></strong> con <a href="https://github.com/ondata/covid19italia/">questo progetto</a></footer>
</body>
</html>