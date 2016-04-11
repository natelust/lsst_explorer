from PyQt4.QtCore import *
from PyQt4.QtGui import *
from NTV.utils import hasCommands
import astropy.wcs as astroWcs
import numpy as np

from .lsst_explorer_ui import Ui_lsst_explorer
from .catalog_view import catalog_view

from lsst.daf.persistence.butler import Butler

@hasCommands("displayExposure", "displayCatalog")
class lsst_explorer(QWidget, Ui_lsst_explorer):
    def __init__(self, main, parent=None):
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.main = main
        self.PropertiesWidget.hide()
        QObject.connect(self.AcceptButton, SIGNAL('clicked()'), self.processInput)

    def processInput(self):
        self.inputRepository = str(self.InputEdit.text())
        exec("temp_dataId = {}".format(str(self.DataIdEdit.text())))
        self.dataId = temp_dataId
        self.imageType = str(self.ImageTypeEdit.text())
        self.catalogType = str(self.CatalogTypeEdit.text())

        self.butler = Butler(self.inputRepository)
        exposure = self.butler.get(self.imageType, self.dataId)
        try:
            self.displayExposure(exposure)
        except:
            pass
        
        if self.catalogType:
            try:
                catalog = self.butler.get(self.catalogType, self.dataId)
                self.displayCatalog(catalog, hasImage=True)
            except:
                pass

    def displayCatalog(self, catalog, hasImage=False):
        self.catalog = catalog
        self.catalogView = catalog_view(catalog, self.main, hasImage)

    def displayExposure(self, exp):
        self.exposure = exp
        self.mi = exp.getMaskedImage()
        # Display the image in the main window
        self.imageArray = self.mi.getImage().getArray()
        self.main.image = self.imageArray
        self.main.head = None
        # Generate colors for the mask planes:
        self.maskPlaneDict = self.exposure.getMaskedImage().getMask().getMaskPlaneDict()
        self.maskPlaneDictKeys = self.maskPlaneDict.keys()
        self.mask = self.mi.getMask().getArray()
        self.bitMask = np.zeros(list(self.imageArray.shape)+[4],dtype=float)
        self.maskColors = {}
        for key in self.maskPlaneDictKeys:
            cmap = np.random.uniform(0,1,3).tolist()+[0.35]
            self.maskColors[key] = cmap
            submask = np.bitwise_and(self.mask, 2**self.maskPlaneDict[key])
            subindex = np.where(submask)
            self.bitMask[subindex] += cmap
        self.main.setup_image_info()
        self.DrawMasks()
        # If the exposure has a wcs set it
        if exp.hasWcs():
            wcs = {a:b for a,b,c in exp.getWcs().getFitsMetadata().toList()}
            self.main.wcs = astroWcs.WCS(wcs)

    def DrawMasks(self):
        # Seperate out displaying the mask incase it must be called again
        self.main.imshow.canvas.ax.imshow(self.bitMask)
        self.main.imshow.canvas.draw()
