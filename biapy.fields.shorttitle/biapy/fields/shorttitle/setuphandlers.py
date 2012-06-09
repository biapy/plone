from Products.CMFCore.utils import getToolByName
from biapy.fields.shorttitle import config

def setupCatalog(portal, indexes=dict(), metadata=list()):
    catalog = getToolByName(portal, 'portal_catalog')

    idxs = catalog.indexes()
    mtds = catalog.schema()
    
    for index in indexes.keys():
        if index not in idxs:
            catalog.addIndex(index, indexes[index])
    
    for mt in metadata:
        if mt not in mtds:
            catalog.addColumn(mt)


def importVarious(self):
    if self.readDataFile('shorttitle.txt') is None:
        return

    portal = self.getSite()
    ptool = getToolByName(portal, 'portal_properties')
    props = ptool.cli_properties

    setupCatalog(portal, indexes=dict(NavigationTitle='FieldIndex'),
                         metadata=['NavigationTitle'])
    
def removeConfiglet(self):
    if self.readDataFile('cli-uninstall.txt') is None:
        return
    portal_conf=getToolByName(self.getSite(),'portal_controlpanel')
    portal_conf.unregisterConfiglet('ContentShortTitle')
