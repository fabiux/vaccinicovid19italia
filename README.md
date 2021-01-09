# Vaccinazioni Covid-19 in Italia

> Basato su dati aperti forniti dal Governo e disponibili [qui](https://github.com/italia/covid19-opendata-vaccini).

## Descrizione

Il software scarica periodicamente i dati necessari, in formato `CSV`, e genera una serie di pagine `HTML` statiche che riportano statistiche sulla fornitura e la somministrazione del vaccino anti-Covid19, a livello regionale e nazionale e su base giornaliera.

Le pagine mostrano i grafici ([ChartJS](https://www.chartjs.org/)) dell'andamento nazionale e regionale delle somministrazioni.

Il sito web risultante è visionabile [qui](https://vaccini.fabiopani.it/).

## Configurazione

Per le configurazioni preferite, vedere i file `import_csv.sh` e `include/config.py`.

Creare un database iniziale utilizzando gli script in `sql/`, come segue:

```bash
sqlite3 vaccini.db < vaccini.sql
sqlite3 vaccini.db < views.sql
```

Inoltre, occorre popolare una prima volta il database con lo script `src/init_db.sh`.

## Licenza d’uso

Vedere il file `LICENSE`.

Per quanto riguarda l'utilizzo dei dati, si veda la licenza del [progetto di origine](https://github.com/italia/covid19-opendata-vaccini).

