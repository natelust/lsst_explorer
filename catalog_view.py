from PyQt4.QtCore import *
from PyQt4.QtGui import *

class LsstQtable(QAbstractTableModel):
    def __init__(self,catalog, parent=None):
        QAbstractTableModel.__init__(self,parent)
        self.catalog = catalog
        self.keys = self.catalog.schema.getNames()

    def rowCount(self,parent):
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

        layout = QVBoxLayout(self)
        layout.addWidget(self.tableView)
        layout.addWidget(self.inputWidget)
        self.setLayout(layout)

        self.tableView.setSelectionBehavior(QTableView.SelectRows)
        self.tableView.doubleClicked.connect(self.viewRecord)
        self.show()

    def goto(self):
        number = int(self.lineNumber.text())
        self.lineNumber.clear()
        self.tableView.selectRow(number)

    def viewRecord(self, index):
        if self.hasImage:
            row = index.row()
            record = self.catalog[row]
            footprint = record.getFootprint().getBBox()
            #import pdb;pdb.set_trace()
            xRange = (footprint.getBeginX()-10, footprint.getMaxX()+10)
            yRange = (footprint.getBeginY()-10, footprint.getMaxY()+10)
            if self.main.orig != 'lower':
                yRange = yRange[::-1]
            extents = (yRange, xRange)
            self.main.set_extents(extents)
            self.main.update_canvas()
        
