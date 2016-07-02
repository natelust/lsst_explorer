from PyQt4.QtCore import *
from PyQt4.QtGui import *
from NTV.utils import hasCommands
import astropy.wcs as astroWcs
import numpy as np

from .lsst_explorer_ui import Ui_lsst_explorer
from .catalog_view import catalog_view

from lsst.daf.persistence.butler import Butler

@hasCommands("displayLsstExposure", "displayLsstCatalog", "displayLsstMaskedImage", "displayLsstImage")
class lsst_explorer(QWidget, Ui_lsst_explorer):
    def __init__(self, main, parent=None):
        QWidget.__init__(self)
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
            self.displayLsstExposure(exposure)
        except:
            pass

        if self.catalogType:
            try:
                catalog = self.butler.get(self.catalogType, self.dataId)
                self.displayLsstCatalog(catalog, hasImage=True)
            except:
                pass

    def displayLsstCatalog(self, catalog, hasImage=False):
        self.catalog = catalog
        self.catalogView = catalog_view(catalog, self.main, hasImage)

    def displayLsstExposure(self, exp):
        self.exposure = exp
        self.mi = exp.getMaskedImage()
        self.displayLsstMaskedImage(self.mi)
        # If the exposure has a wcs set it
        if exp.hasWcs():
            wcs = {a:b for a,b,c in exp.getWcs().getFitsMetadata().toList()}
            self.main.wcs = astroWcs.WCS(wcs)

    def displayLsstMaskedImage(self, maskedImage):
        self.displayLsstImage(maskedImage.getImage())
        self.DrawMasks(maskedImage.getMask())

    def displayLsstImage(self, image):
        self.imageArray = image.getArray()
        self.main.image = self.imageArray
        self.main.head = None
        self.main.funloaded = 1
        self.main.setup_image_info()

    def DrawMasks(self, mask):
        # Seperate out displaying the mask incase it must be called again
        self.maskPlaneDict = mask.getMaskPlaneDict()
        self.maskPlaneDictKeys = self.maskPlaneDict.keys()
        self.mask = mask.getArray()
        tmask = []
        tkeys = []
        for key in self.maskPlaneDictKeys:
            submask = np.bitwise_and(self.mask, 2**self.maskPlaneDict[key])
            tmask.append(submask)
            tkeys.append(key)
        self.main.clear_mask()
        self.main.add_mask(tmask, tkeys)
