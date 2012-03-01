from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.schema.vocabulary import SimpleVocabulary
from zope.component import getUtility
from zope.schema.vocabulary import SimpleTerm
from zope.i18n import translate

from biapy.fields.shorttitle.shorttitleprefs import IShortTitlePrefsForm
from biapy.fields.shorttitle import config
from biapy.fields.shorttitle import ShortTitleMessageFactory as _

