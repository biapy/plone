from zope import schema
from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer

from biapy.fields.shorttitle import ShortTitleMessageFactory as _


class IShortTitleSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """

class IShortTitleable(Interface):
    """ marker interface """

