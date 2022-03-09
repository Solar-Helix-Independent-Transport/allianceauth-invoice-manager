from allianceauth.services.hooks import MenuItemHook, UrlHook
from django.utils.translation import gettext_lazy as _
from allianceauth import hooks

from .models import Invoice
from . import app_settings
from . import urls


class Invoices(MenuItemHook):
    def __init__(self):
        MenuItemHook.__init__(self,
                              app_settings.INVOICES_APP_NAME,
                              'fas fa-file-invoice-dollar fa-fw',
                              'invoices:r_list',
                              navactive=['invoices:'])

    def render(self, request):
        if request.user.has_perm('invoices.access_invoices') or request.user.has_perm('invoices.view_corp') or request.user.has_perm('invoices.view_alliance') or request.user.has_perm('invoices.view_all'):
            chars = request.user.character_ownerships.all().values_list('character')
            inv_count = Invoice.objects.visible_to(request.user).filter(
                paid=False, character__in=chars).count()
            if inv_count:
                self.count = inv_count
            return MenuItemHook.render(self, request)
        return ''


@hooks.register('menu_item_hook')
def register_menu():
    return Invoices()


@hooks.register('url_hook')
def register_url():
    return UrlHook(urls, 'invoices', r'^invoice/')
