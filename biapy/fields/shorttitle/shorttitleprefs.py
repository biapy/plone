from zope.interface import Interface, implements
from zope.component import adapts
from zope.component import getUtility
from zope.component import getMultiAdapter

from zope.formlib import form
from zope import schema
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.interfaces import IPropertiesTool
from Products.CMFCore.utils import getToolByName
from plone.app.controlpanel.form import ControlPanelForm
from plone.app.form.validators import null_validator

from Products.statusmessages.interfaces import IStatusMessage
from plone.protect import CheckAuthenticator
from zope.event import notify
from plone.app.controlpanel.events import ConfigurationChangedEvent

from Products.CMFPlone import PloneMessageFactory as _p
from biapy.fields.shorttitle import ShortTitleMessageFactory as _
from biapy.fields.shorttitle.interfaces import IShortTitleable
from biapy.fields.shorttitle import config
from ZODB.POSException import ConflictError


class IShortTitlePrefsForm(Interface):    
    """ The view for ShortTitle prefs form. """

    allowed_types = schema.Tuple(title=_(u'Portal types'),
                          description=_(u'Portal types short title may be attached to.'),
                          missing_value=tuple(),
                          value_type=schema.Choice(
                                   vocabulary="plone.app.vocabularies.UserFriendlyTypes"),
                          required=False)



class ShortTitleControlPanelAdapter(SchemaAdapterBase):
    """ Control Panel adapter """

    adapts(IPloneSiteRoot)
    implements(IShortTitlePrefsForm)
    
    def __init__(self, context):
        super(ShortTitleControlPanelAdapter, self).__init__(context)
        pprop = getUtility(IPropertiesTool)
        self.cli_props = getattr(pprop, 'cli_properties', None)
        self.context = context

    def get_allowed_types(self):
        return self.cli_props.allowed_types
        
    def set_allowed_types(self, allowed_types):
        self.cli_props.allowed_types = allowed_types

    allowed_types = property(get_allowed_types, set_allowed_types)



class ShortTitlePrefsForm(ControlPanelForm):
    """ The view class for the ShortTitle preferences form. """

    implements(IShortTitlePrefsForm)
    form_fields = form.FormFields(IShortTitlePrefsForm)

    label = _(u'Short Title field Settings Form')
    description = _(u'Select properties for Short Title field')
    form_name = _(u'Short Title field Settings')
            
    # handle_edit_action and handle_cancel_action are copied from 
    # ControlPanelForm because they are overriden by my handle_scales_action
    @form.action(_p(u'label_save', default=u'Save'), name=u'save')
    def handle_edit_action(self, action, data):
        CheckAuthenticator(self.request)
        if form.applyChanges(self.context, self.form_fields, data,
                             self.adapters):
            self.status = _p("Changes saved.")
            notify(ConfigurationChangedEvent(self, data))
            self._on_save(data)
        else:
            self.status = _p("No changes made.")

    @form.action(_p(u'label_cancel', default=u'Cancel'),
                 validator=null_validator,
                 name=u'cancel')
    def handle_cancel_action(self, action, data):
        IStatusMessage(self.request).addStatusMessage(_p("Changes canceled."),
                                                      type="info")
        url = getMultiAdapter((self.context, self.request),
                              name='absolute_url')()
        self.request.response.redirect(url + '/plone_control_panel')
        return ''

