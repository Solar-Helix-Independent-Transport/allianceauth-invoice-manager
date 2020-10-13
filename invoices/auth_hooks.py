from allianceauth.services.hooks import MenuItemHook, UrlHook
from django.utils.translation import ugettext_lazy as _
from allianceauth import hooks
from . import urls

class Invoices(MenuItemHook):
    def __init__(self):
        MenuItemHook.__init__(self,
                              _('Invoices'),
                              'fas fa-file-invoice-dollar fa-fw',
                              'invoices:list',
                              navactive=['corptools:'])

    def render(self, request):
        if request.user.has_perm('invoices.access_invoices') or request.user.has_perm('invoices.view_corp') or request.user.has_perm('invoices.view_alliance') or request.user.has_perm('invoices.view_all'):
            return MenuItemHook.render(self, request)
        return ''

@hooks.register('menu_item_hook')
def register_menu():
    return Invoices()

@hooks.register('url_hook')
def register_url():
    return UrlHook(urls, 'invoices', r'^invoice/')
