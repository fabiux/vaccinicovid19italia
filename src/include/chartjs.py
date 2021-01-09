"""
Class ChartJS (time series).
"""
from datetime import datetime, timedelta


class DataSet(object):
    def __init__(self, varname, label, bgcolor, bordercolor, borderwidth=1, hidden=False):
        """
        :param varname: name of javascript var name
        :param label: label for this data series
        :param bgcolor: background color
        :param bordercolor: border color
        :param borderwidth: border width

        colors are dict structures with following fields:
        - r: 0 - 255
        - g: 0 - 255
        - b: 0 - 255
        - a: 0.0 - 1.0
        """
        self._varname = varname
        self._label = label
        self._bgcolor = bgcolor
        self._bordercolor = bordercolor
        self._borderwidth = borderwidth
        self._hidden = hidden

    @staticmethod
    def _rgba(color):
        return "'rgba({}, {}, {}, {})'".format(color['r'], color['g'], color['b'], color['a'])

    @property
    def js(self):
        """
        Javascript equivalent for this data series.
        """
        hdn = 'hidden: true, ' if self._hidden else ''
        return "{" + "label: '{}', {}fill: true, lineTension: 0, data: {}, backgroundColor: {}, borderColor: {}, borderWidth: {}".format(self._label, hdn, self._varname, self._rgba(self._bgcolor), self._rgba(self._bordercolor), self._borderwidth) + "}"


class ChartJS(object):
    def __init__(self, element_id, mintime, maxtime, chart_type='line', chart_title='', labels=[]):
        """
        :param element_id: DOM element id containing the chart
        :param mintime: starting date ('YYYY-MM-DD')
        :param mintime: ending date ('YYYY-MM-DD')
        :param chart_type: chart type - FIXME list here
        FIXME il numero di label deve coincidere con il numero di valori delle singole serie.
        """
        self._element_id = element_id
        self._chart_type = chart_type
        self._chart_title = chart_title
        self._values = []
        self._dsets = []
        if labels == []:
            self._labels = ['"{}"'.format(mintime)]
            currtime = mintime
            while currtime < maxtime:
                d = datetime(int(currtime[:4]), int(currtime[5:7]), int(currtime[8:10]), 0, 0)
                d = d + timedelta(days=1)
                currtime = str(d)[:10]
                self._labels.append('"{}"'.format(currtime))
        else:
            self._labels = labels

    def add_dataset(self, data, varname, label, bgcolor, bordercolor, borderwidth=1, hidden=False):
        """
        Adds a dataset to this chart.
        :param data (list): data value list
        :param varname: javascript var name
        :param label: label for this dataset
        :param bgcolor: background color
        :param bordercolor: border color
        :param borderwidth: border width
        """
        self._values.append(dict(varname=varname, data=data))
        dset = DataSet(varname, label, bgcolor, bordercolor, borderwidth, hidden=hidden)
        self._dsets.append(dset.js)

    @property
    def js(self):
        """
        Javascript equivalent for this chart.
        """
        s = 'var labels = [{}];\n'.format(','.join(self._labels))
        for v in self._values:
            s += 'var {} = {};\n'.format(v['varname'], repr(v['data']).replace(' ', ''))
        s += "var config = {\n"
        s += "    type: '{}',\n".format(self._chart_type)
        s += "    data: {\n"
        s += "        labels: labels,\n"
        s += "        datasets: [{}]\n".format(','.join(self._dsets))
        s += "    },\n"
        s += "    options: {\n"
        s += "        responsive: true,\n"
        s += "        tooltips: {mode: 'index', intersect: false},\n"
        s += "        hover: {mode: 'nearest', intersect: true},\n"
        if self._chart_title != '':
            s += "        title: {display: true, text: '" + self._chart_title + "'},\n"
        s += "        scales: {\n"
        s += "            yAxes: [{\n"
        s += "                ticks: {\n"
        s += "                    beginAtZero: true\n"
        s += "                },\n"
        s += "                scaleLabel: {display: true, labelString: ''}\n"
        s += "            }],\n"
        s += "            xAxes: [{}]\n"
        s += "        }\n"
        s += "    }\n"
        s += "};\n\n"
        s += "window.onload = function() {\n"
        s += "    var ctx = document.getElementById('mygraph').getContext('2d');\n"
        s += "    window.myChart = new Chart(ctx, config);\n"
        s += "};\n"
        return s
