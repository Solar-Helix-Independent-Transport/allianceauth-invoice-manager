import logging
import os 

from celery import shared_task
from allianceauth.eveonline.models import EveCharacter, EveCorporationInfo, EveAllianceInfo
from django.utils import timezone
from . import app_settings
from .models import Invoice
from corptools.models import CorporationWalletJournalEntry
from allianceauth.services.tasks import QueueOnce

logger = logging.getLogger(__name__)

@shared_task(bind=True, base=QueueOnce)
def check_for_payments(self):
    logger.debug("Checking for payments")

    invoices = Invoice.objects.filter(paid=False)
    refs = invoices.values_list('invoice_ref')
    payments = CorporationWalletJournalEntry.objects.filter(division__corporation__corporation__corporation_id=app_settings.PAYMENT_CORP,
                                                            reason__in=refs,
                                                            amount__gt=1)
    payment_dict = {}
    for payment in payments:
        if payment.reason not in payment_dict:
            payment_dict[payment.reason] = []
        payment_dict[payment.reason].append(payment)

    for invoice in invoices:
        if invoice.invoice_ref in payment_dict:
            logger.debug("Payment Found!")
            payment_totals = 0
            for p in payment_dict[payment.reason]:
                payment_totals += p.amount
            
            if payment_totals >= invoice.amount:
                invoice.paid = True
                invoice.payment = payment_dict[payment.reason][0]
                invoice.save()
                invoice.notify("Payment Received", "Paid")
