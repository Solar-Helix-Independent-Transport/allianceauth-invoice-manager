from django.conf import settings
from django.contrib import admin

from invoices import models

# Register your models here.
from .models import Invoice


@admin.register(Invoice)
class InvoicesAdmin(admin.ModelAdmin):

    list_select_related = True
    list_display = ['character', 'invoice_ref',
                    'amount', 'paid', 'marked_paid_by']
    search_fields = ('character__character_name', 'invoice_ref',
                     'marked_paid_by__character_name')
    raw_id_fields = ('character', 'payment')


if 'securegroups' in settings.INSTALLED_APPS:
    admin.site.register(models.NoOverdueFilter)
    admin.site.register(models.TotalInvoicesFilter)
