"""
Helper functions.
"""
from include.config import logger, tpldir, distdir


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
