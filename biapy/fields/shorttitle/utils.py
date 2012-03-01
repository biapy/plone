from biapy.fields.shorttitle.interfaces import IShortTitleable
from biapy.fields.shorttitle.config import SHORT_TITLE_FIELD_NAME

from plone.indexer import indexer
from zope.component import provideAdapter

@indexer(IShortTitleable)
def NavigationTitle(obj):
    field = obj.getField(SHORT_TITLE_FIELD_NAME)
    if field is not None:
        value = field.get(obj)
        if value:
          return value
    field = obj.getField('title')
    if field is not None:
        value = field.get(obj)
        return value
provideAdapter(NavigationTitle, name='NavigationTitle')

