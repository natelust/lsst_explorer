from PyQt4.QtCore import *
from PyQt4.QtGui import *
import re
import numpy as np
import itertools
from collections import OrderedDict
import textwrap
import matplotlib as mpl
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg,
                                                NavigationToolbar2QT)

from .expressionParser import expressionEvaluator


class LsstCatalogPlot(QDialog):
    def __init__(self, main, ind, dep, color):
        QDialog.__init__(self, main)
        self.main = main
        self.setPalette(main.palette())
        self.ind = ind
        self.dep = dep
        self.color = color
        self.info = QLabel('Click on a point to highlight the corresponding'
                           ' record')
        self.figure = mpl.figure.Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setParent(self)
        self.canvas.setFocus()

        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        self.ax = self.figure.add_subplot(111)
        self.scatterPlot = self.ax.scatter(self.ind, self.dep, c=self.color,
                                           picker=5, cmap=mpl.cm.YlGnBu_r)
        if self.color is not None:
            self.colorbar = self.figure.colorbar(self.scatterPlot)

        self.canvas.mpl_connect('pick_event', self.main.handleClick)

        vbox = QVBoxLayout()
        vbox.addWidget(self.info)
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.toolbar)
        self.setLayout(vbox)

        self.show()


class LsstCatalogPlotter(QWidget):
    def __init__(self, catalog, main):
        QObject.__init__(self)

        self.catalog = catalog
        self.main = main
        self.setPalette(main.palette())
        self.catalogEnum = OrderedDict((i, col) for i, col in
                                       enumerate(catalog.schema.getNames()))

        self.layout = QVBoxLayout()

        descriptionText = '''
        In the following fields expressions can be entered which may use
        the following operators + , - , * , / , ** , log. Variables must
        be a column in the table, and are spcified as <num> where num is
        the number of the column.
        '''
        descriptionLabel = QLabel(textwrap.dedent(descriptionText))
        indLabel = QLabel("Independent variable")
        depLabel = QLabel("Dependent variable")
        colorLabel = QLabel("Color by (Must be convertable to number)")

        self.indEntry = QLineEdit()
        self.depEntry = QLineEdit()
        self.colorEntry = QLineEdit()
        self.goButton = QPushButton("Plot")
        self.goButton.pressed.connect(self.processAndPlot)
        self.goButton.setAutoDefault(False)

        self.layout.addWidget(descriptionLabel)
        self.layout.addWidget(indLabel)
        self.layout.addWidget(self.indEntry)
        self.layout.addWidget(depLabel)
        self.layout.addWidget(self.depEntry)
        self.layout.addWidget(colorLabel)
        self.layout.addWidget(self.colorEntry)
        self.layout.addWidget(self.goButton)

        self.setLayout(self.layout)

    def extractStringInfo(self, text):
        numbers = re.compile('<(\d+)>*').findall(text)
        if len(numbers) == 0:
            raise ValueError('No variables detected')
        variables = [self.catalog.get(self.catalogEnum[int(x)])
                     for x in numbers]
        return numbers, variables

    def modStringAndDict(self, string, numbers, variables, ident, mask):
        newString = string
        parserDict = {}
        for i, (num, var) in enumerate(zip(numbers, variables)):
            newString = newString.replace('<{}>'.format(num),
                                          '{}{}'.format(ident, i))
            parserDict['{}{}'.format(ident, i)] = var.astype('float')[mask]
        return newString, parserDict

    def processAndPlot(self):
        try:
            indString = str(self.indEntry.text())
            indNumbers, indVars = self.extractStringInfo(indString)

            depString = str(self.depEntry.text())
            depNumbers, depVars = self.extractStringInfo(depString)

            colorString = str(self.colorEntry.text())
            doColor = True if len(str(colorString)) > 0 else False

            if doColor:
                colorNumbers, colorVars = self.extractStringInfo(colorString)
            else:
                colorNumbers, colorVars = ([], [])

            self.maskArray = np.ones(len(self.catalog), dtype=bool)

            for value in itertools.chain(indVars, depVars, colorVars):
                self.maskArray *= np.isfinite(value.astype('float'))

            parserDict = {}
            newIndString, tdict = self.modStringAndDict(indString, indNumbers,
                                                        indVars, 'i',
                                                        self.maskArray)
            parserDict.update(tdict)

            newDepString, tdict = self.modStringAndDict(depString, depNumbers,
                                                        depVars, 'd',
                                                        self.maskArray)
            parserDict.update(tdict)

            newColorString, tdict = self.modStringAndDict(colorString,
                                                          colorNumbers,
                                                          colorVars, 'c',
                                                          self.maskArray)

            parserDict.update(tdict)

            indArray = expressionEvaluator(newIndString, **parserDict)
            depArray = expressionEvaluator(newDepString, **parserDict)
            if doColor:
                colorArray = expressionEvaluator(newColorString, **parserDict)
            else:
                colorArray = None

        except Exception as e:
            print(e)
        self.plot = LsstCatalogPlot(self, indArray, depArray, colorArray)

    def handleClick(self, event):
        entry = event.ind[0]
        unMaskedEntry = np.arange(len(self.catalog),
                                  dtype=int)[self.maskArray][entry]
        self.main.tableView.selectRow(unMaskedEntry)
