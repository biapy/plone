from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from archetypes.schemaextender.field import ExtensionField
from zope.component import adapts
from zope.component import getUtility
from zope.interface import implements
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from Products.Archetypes.public import ImageWidget
from Products.Archetypes.public import AnnotationStorage
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.ATContentTypes.configuration import zconf

from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces.http import IHTTPRequest
from ZPublisher.BaseRequest import DefaultPublishTraverse
from Products.validation import V_REQUIRED


from biapy.fields.shorttitle.interfaces import IShortTitleable
from biapy.fields.shorttitle.interfaces import IShortTitleSpecific
from biapy.fields.shorttitle import ShortTitleMessageFactory as _
from biapy.fields.shorttitle.config import SHORT_TITLE_FIELD_NAME
from biapy.fields.shorttitle.shorttitleprefs import IShortTitlePrefsForm

class ShortTitleField(ExtensionField, StringField):
    """ A trivial string field """

class ShortTitleExtender(object):
    adapts(IShortTitleable)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)

    layer = IShortTitleSpecific

    fields = [

            ShortTitleField(SHORT_TITLE_FIELD_NAME,
                required=False,
                searchable=False,
                storage = AnnotationStorage(),
                languageIndependent = False,
                widget = StringWidget(
                            label=_(u"Short title"),
                            description=_(u"Short title for navigation"),
                        ),
            ),

        ]

    def __init__(self, context):
         self.context = context

    def getFields(self):
        portal = getUtility(IPloneSiteRoot)
        cli_prefs = IShortTitlePrefsForm(portal)
        if cli_prefs.cli_props is not None:
            portal_type = getattr(self.context, 'portal_type', None)
            if portal_type in cli_prefs.allowed_types:
                return self.fields
        return []

    def getOrder(self, original):
        """
        'original' is a dictionary where the keys are the names of
        schemata and the values are lists of field names, in order.

        Move shortTitle field just after the Title
        """
        default = original.get('default', None)
        if default:
            title_index = 0
            # if there is no title nor description field, do nothing
            if 'title' in default:
              title_index = default.index('title')
            if title_index >= 0 and (SHORT_TITLE_FIELD_NAME in default):
                default.remove(SHORT_TITLE_FIELD_NAME)
                default.insert(title_index+1, SHORT_TITLE_FIELD_NAME)
        return original

