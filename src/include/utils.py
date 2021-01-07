"""
Helper functions.
"""
from include.config import logger, tpldir, distdir, ds_root_url, ds_files, csvdir
from csv import DictReader
import requests
from time import sleep


def read_template(name):
    """
    Restituisce il contenuto di un template.
    """
    try:
        with open(tpldir + name + '.tpl', 'r') as f:
            html = f.read()
        return html
    except Exception as e:
        logger.error('read_template() - name = {}: {}'.format(name, str(e)))
        return ''


def write_html(name, html):
    """
    Scrive un file HTML statico.
    """
    try:
        with open(distdir + name + '.html', 'w') as f:
            f.write(html)
    except Exception as e:
        logger.error('write_html() - name = {}: {}'.format(name, str(e)))


def read_csv(filename):
    """
    Read csvfile and return FIXME.
    """
    with open(csvdir + filename, newline='') as f:
        reader = DictReader(f)
        return [row for row in reader]


def save_file(fname, content):
    """
    FIXME
    """
    with open(fname, 'w') as f:
        f.write(content)


def download_dataset():
    """
    Scarica i dataset (solo i file che ci servono).
    """
    for csvfile in ds_files:
        try:
            sleep(2)
            r = requests.get(ds_root_url + csvfile + '.csv')
            if r.status_code < 300:
                save_file(csvdir + csvfile + '.csv', r.text)
        except Exception as e:
            logger.error('download_dataset() - csvfile = {}: {}'.format(csvfile, str(e)))
