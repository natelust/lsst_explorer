from PyQt4.QtCore import *
from PyQt4.QtGui import *

class LsstQtable(QAbstractTableModel):
    def __init__(self, catalog, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.catalog = catalog
        self.keys = self.catalog.schema.getNames()

    def rowCount(self, parent):
        return len(self.catalog)

    def columnCount(self, parent):
        return len(self.keys)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                key = self.keys[index.column()]
                return self.catalog[index.row()].get(key)
        return None

    def headerData(self, p_int, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.keys[p_int]
            elif orientation == Qt.Vertical:
                return p_int
        return None

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


class catalog_view(QDialog):
    def __init__(self, catalog, main, hasImage=False, parent=None):
        QDialog.__init__(self)
        self.setModal(False)
        self.catalog = catalog
        self.main = main
        self.hasImage = hasImage
        self.qCatalog = LsstQtable(catalog)
        self.tableView = QTableView()
        self.tableView.setModel(self.qCatalog)
        self.schemaEnum = {name: i for i, name in
                           enumerate(catalog.schema.getNames())}

        # Add in checkboxes for all the table columns
        self.checkboxWidget = QWidget()
        self.checkboxWidget.setMaximumWidth(500)
        checkboxLayout = QVBoxLayout(self)
        allCheckButton = QCheckBox('All')
        allCheckButton.setChecked(True)
        allCheckButton.stateChanged.connect(self.updateTableAll)
        checkboxLayout.addWidget(allCheckButton)
        self.checkButtons = []
        for i, name in enumerate(self.catalog.schema.getNames()):
            tmp = QCheckBox("{}: {}".format(i, name))
            tmp.setChecked(True)
            tmp.stateChanged.connect(self.updateTable)
            checkboxLayout.addWidget(tmp)
            self.checkButtons.append(tmp)
        self.checkboxWidget.setLayout(checkboxLayout)
        self.scroller = QScrollArea()
        self.scroller.setWidget(self.checkboxWidget)
        self.scroller.setWidgetResizable(True)

        self.inputWidget = QWidget()
        inputLayout = QHBoxLayout(self)
        self.lineLabel = QLabel("Jump to row")
        self.lineNumber = QLineEdit()
        self.lineButton = QPushButton()
        self.lineButton.clicked.connect(self.goto)
        self.lineButton.setText('Go')
        inputLayout.addWidget(self.lineLabel)
        inputLayout.addWidget(self.lineNumber)
        inputLayout.addWidget(self.lineButton)
        self.inputWidget.setLayout(inputLayout)

        self.selectWidget = QWidget()
        msg = "Click button enable selecting record from image,"\
              " will fail if no unique record found"
        self.selectLabel = QLabel(msg)
        self.selectButton = QPushButton("Go")
        self.selectWidthLabel = QLabel("Enter width in pixels to concider")
        self.selectLineEdit = QLineEdit("5")
        selectLayout = QVBoxLayout(self)
        selectLayout.addWidget(self.selectLabel)
        selectLayout.addWidget(self.selectWidthLabel)
        selectLayout.addWidget(self.selectLineEdit)
        selectLayout.addWidget(self.selectButton)
        self.selectWidget.setLayout(selectLayout)
        self.selectButton.clicked.connect(self.getClick)

        layout = QVBoxLayout(self)
        layout.addWidget(self.tableView)
        layout.addWidget(self.scroller)
        layout.addWidget(self.inputWidget)
        layout.addWidget(self.selectWidget)
        self.setLayout(layout)

        # Generate the mapping
        self.xdict = {}
        self.ydict = {}
        for i in range(len(catalog)):
            x = int(catalog[i].getX())
            y = int(catalog[i].getY())
            if x not in self.xdict:
                self.xdict[x] = set()
            self.xdict[x].add(i)
            if y not in self.ydict:
                self.ydict[y] = set()
            self.ydict[y].add(i)

        self.tableView.setSelectionBehavior(QTableView.SelectRows)
        self.tableView.doubleClicked.connect(self.viewRecord)
        self.show()

    def updateTableAll(self, state):
        for box in self.checkButtons:
            box.setChecked(state)

    def updateTable(self, state):
        sender = self.sender()
        columNumber = self.schemaEnum[str(sender.text())]
        if state:
            self.tableView.showColumn(columNumber)
        else:
            self.tableView.hideColumn(columNumber)

    def getClick(self):
        if self.hasImage:
            self.main.connectclick(self.tableLookup)

    def goto(self):
        number = int(self.lineNumber.text())
        self.lineNumber.clear()
        self.tableView.selectRow(number)

    def viewRecord(self, index):
        if self.hasImage:
            row = index.row()
            record = self.catalog[row]
            footprint = record.getFootprint().getBBox()
            xRange = (footprint.getBeginX()-10, footprint.getMaxX()+10)
            yRange = (footprint.getBeginY()-10, footprint.getMaxY()+10)
            if self.main.orig != 'lower':
                yRange = yRange[::-1]
            extents = (yRange, xRange)
            self.main.set_extents(extents)
            self.main.update_canvas()

    def tableLookup(self, event):
        x = int(event.xdata)
        y = int(event.ydata)

        span = int(self.selectLineEdit.text())

        yRange = range(y-span, y+span+1)
        xRange = range(x-span, x+span+1)

        ySetCollection = []
        xSetCollection = []
        for i in range(len(yRange)):
            if yRange[i] in self.ydict:
                ySetCollection.append(self.ydict[yRange[i]])
            if xRange[i] in self.xdict:
                xSetCollection.append(self.xdict[xRange[i]])

        if len(ySetCollection) == 0 or len(xSetCollection) == 0:
            return
        ySet = set()
        xSet = set()
        for s in ySetCollection:
            ySet = s | ySet
        for s in xSetCollection:
            xSet = s | xSet

        result = ySet & xSet

        if len(result) == 1:
            self.tableView.selectRow(list(result)[0])
        else:
            return
