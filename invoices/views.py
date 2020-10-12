import os

from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from .models import Invoice
@login_required
def show_invoices(request):
    invoices = Invoice.objects.visible_to(request.user).filter(paid=False)
    outstanding_isk = invoices.aggregate(total_isk=Sum('amount'))
    completed_invoices = Invoice.objects.visible_to(request.user).filter(paid=True).order_by('-due_date')[:100]
    
    ctx = { 'invoices':invoices, 
            'outstanding_isk': outstanding_isk['total_isk'],
            'complete_invoices':completed_invoices}

    return render(request, 'invoices/list.html', context=ctx)
