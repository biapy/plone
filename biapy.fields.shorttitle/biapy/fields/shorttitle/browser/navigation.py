from plone.memoize.instance import memoize
from zope.component import getMultiAdapter, queryUtility

from plone.i18n.normalizer.interfaces import IIDNormalizer

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils

from plone.app.portlets.portlets.navigation import Renderer, NavtreeStrategy

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ShortTitleNavtreeStrategy(NavtreeStrategy):
    """The navtree strategy used for the ShortTitle navigation portlet
    """

    def decoratorFactory(self, node):
        context = aq_inner(self.context)
        request = context.REQUEST

        newNode = node.copy()
        item = node['item']

        portalType = getattr(item, 'portal_type', None)
        itemUrl = item.getURL()
        if portalType is not None and portalType in self.viewActionTypes:
            itemUrl += '/view'

        useRemoteUrl = False
        getRemoteUrl = getattr(item, 'getRemoteUrl', None)
        isCreator = self.memberId == getattr(item, 'Creator', None)
        if getRemoteUrl and not isCreator:
            useRemoteUrl = True
        
        isFolderish = getattr(item, 'is_folderish', None)
        showChildren = False
        if isFolderish and (portalType is None or portalType not in self.parentTypesNQ):
            showChildren = True

        ploneview = getMultiAdapter((context, request), name=u'plone')

        newNode['Title'] = getattr(item, 'NavigationTitle', None) or utils.pretty_title_or_id(context, item)
        newNode['id'] = item.getId
        newNode['UID'] = item.UID
        newNode['absolute_url'] = itemUrl
        newNode['getURL'] = itemUrl
        newNode['path'] = item.getPath()
        newNode['item_icon'] = ploneview.getIcon(item)
        newNode['Creator'] = getattr(item, 'Creator', None)
        newNode['creation_date'] = getattr(item, 'CreationDate', None)
        newNode['portal_type'] = portalType
        newNode['review_state'] = getattr(item, 'review_state', None)
        newNode['Description'] = getattr(item, 'Description', None)
        newNode['show_children'] = showChildren
        newNode['no_display'] = False # We sort this out with the nodeFilter
        # BBB getRemoteUrl and link_remote are deprecated, remove in Plone 4
        newNode['getRemoteUrl'] = getattr(item, 'getRemoteUrl', None)
        newNode['useRemoteUrl'] = useRemoteUrl
        newNode['link_remote'] = newNode['getRemoteUrl'] and newNode['Creator'] != self.memberId

        idnormalizer = queryUtility(IIDNormalizer)
        newNode['normalized_portal_type'] = idnormalizer.normalize(portalType)
        newNode['normalized_review_state'] = idnormalizer.normalize(newNode['review_state'])
        newNode['normalized_id'] = idnormalizer.normalize(newNode['id'])

        return newNode
