from django.db import models
from allianceauth.eveonline.models import EveCharacter

from corptools.models import CorporationWalletJournalEntry

from . import app_settings
from .managers import InvoiceManager

if app_settings.discord_bot_active():
    import aadiscordbot

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
        return "{} - {} - {}".format(self.character.character_name, self.invoice_ref, self.amount)

    class Meta:
        permissions = (('view_corp', 'Can View Own Corps Invoices'),
                       ('view_alliance', 'Can View Oen Alliances Invoices'),
                       ('view_all', 'Can View All Invoices'),
                      )