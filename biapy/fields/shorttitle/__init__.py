from zope.i18n import MessageFactory
ShortTitleMessageFactory = MessageFactory('biapy.fields.shorttitle')

# import utils to register indexable attribute
import utils

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
