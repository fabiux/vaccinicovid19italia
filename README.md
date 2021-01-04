# Vaccinazioni Covid-19 in Italia

> Basato su [questo progetto](https://github.com/ondata/covid19italia/), a cura di [OnData](https://ondata.it/), che libera (fra l'altro) i dati relativi alle forniture e somministrazioni dei vaccini anti-Covid19, su base regionale.

## Descrizione

Il software scarica periodicamente i dati in oggetto, in formato `CSV`, e genera una serie di pagine `HTML` statiche che riportano statistiche sulla fornitura e la somministrazione del vaccino anti-Covid19, a livello regionale e nazionale e su base giornaliera.

Le pagine mostrano i grafici ([ChartJS](https://www.chartjs.org/)) dell'andamento nazionale e regionale delle somministrazioni.

Il sito web risultante è visionabile [qui](https://vaccini.fabiopani.it/).

## Configurazione

Per le configurazioni preferite, vedere i file `import_csv.sh` e `include/config.py`.

Creare un database iniziale utilizzando gli script in `sql/`, come segue:

```bash
sqlite3 vaccini.db < vaccini.sql
sqlite3 vaccini.db < views.sql
```

## Licenza d’uso

Vedere il file `LICENSE`.

Per quanto riguarda l'utilizzo dei dati, si veda la licenza del [progetto di origine](https://github.com/ondata/covid19italia/).

