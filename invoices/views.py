import os

from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from .models import Invoice
@login_required
def show_invoices(request):
    chars = request.user.character_ownerships.all().values_list('character')
    admin_invoices = Invoice.objects.visible_to(request.user).filter(paid=False).exclude(character__in=chars)
    invoices = Invoice.objects.visible_to(request.user).filter(paid=False, character__in=chars)
    outstanding_isk = invoices.aggregate(total_isk=Sum('amount'))
    admin_isk = admin_invoices.aggregate(total_isk=Sum('amount'))
    completed_invoices = Invoice.objects.visible_to(request.user).filter(paid=True, character__in=chars).order_by('-due_date')[:10]
    if outstanding_isk['total_isk'] == None:
        outstanding = 0
    else:
        outstanding = outstanding_isk['total_isk']

    ctx = { 'invoices':invoices, 
            'admin_invoices':admin_invoices,
            'admin_isk': admin_isk['total_isk'],
            'outstanding_isk': outstanding,
            'complete_invoices':completed_invoices}

    return render(request, 'invoices/list.html', context=ctx)
