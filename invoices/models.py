from django.db import models
from allianceauth.eveonline.models import EveCharacter
from allianceauth.notifications import notify as auth_notify
from corptools.models import CorporationWalletJournalEntry
from django.urls import reverse

from . import app_settings
from .managers import InvoiceManager
from django.utils import timezone

if app_settings.discord_bot_active():
    from aadiscordbot import tasks as bot_tasks

import logging
logger = logging.getLogger(__name__)

class Invoice(models.Model):

    objects = InvoiceManager()

    character = models.ForeignKey(EveCharacter, null=True, default=None, on_delete=models.SET_NULL, related_name='invoices')
    amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, default=None)
    invoice_ref = models.CharField(max_length=72)
    due_date= models.DateTimeField()
    notified = models.DateTimeField(null=True, default=None, blank=True)

    paid = models.BooleanField(default=False, blank=True)
    payment = models.OneToOneField(CorporationWalletJournalEntry, blank=True, null=True, default=None, on_delete=models.SET_NULL, related_name='invoice')

    note = models.TextField(blank=True, null=True, default=None,)

    def __str__(self):
        return "{} - {} - {}".format(self.character, self.invoice_ref, self.amount)

    @property
    def is_past_due(self):
        return timezone.now() > self.due_date

    def notify(self, message, title="Contributions Bot Message"):
        url = reverse("invoices:r_list")
        u = self.character.character_ownership.user
        message = "Invoice:{} Ƶ{:.2f}\n{}\n{}{}".format(
            self.invoice_ref,
            self.amount,
            message,
            app_settings.get_site_url(),
            url
        )
        if app_settings.discord_bot_active(): 
            try:
                bot_tasks.send_direct_message.delay(u.discord.uid, message)
            except Exception as e:
                logger.error(e, exc_info=True)
                pass
        auth_notify(
            u, 
            title,
            message,
            'info'
        )

    class Meta:
        permissions = (('view_corp', 'Can View Own Corps Invoices'),
                       ('view_alliance', 'Can View Own Alliances Invoices'),
                       ('view_all', 'Can View All Invoices'),
                       ('access_invoices', 'Can Access the Invoice App')
                      )
